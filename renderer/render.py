from PIL import Image
from re import compile
from pathlib import Path

fenre = compile(r"^[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}/[rnbqkpRNBQKP1-8]{,8}$")

white = "PNBRQK"
black = white.lower()

chars = {
    "r": "rook",
    "n": "knight",
    "b": "bishop",
    "q": "queen",
    "k": "king",
    "p": "pawn"
}

cache = set()


class Piece:
    def __init__(self, name: str = None, colour: str = None, code: str = None):
        self.name = name
        self.colour = colour
        self.code = code

        self.filename = f"./static/{name}_{colour}.png"

    def __str__(self):
        if not self.name:
            return " "
        return self.code

    def __repr__(self):
        return str(self)


class Board:
    def __init__(self, fen: str):
        self.b = self.parse_fen(fen)

    @staticmethod
    def parse_fen(fen: str):
        if not fenre.match(fen):
            raise Exception("Invalid FEN")
        pieces = []

        for l in fen.split("/"):
            line = []

            for char in l:
                if char.isdigit():
                    for i in range(int(char)):
                        line.append(Piece())
                elif char in white:
                    line.append(Piece(chars[char.lower()], "white", char))
                else:
                    line.append(Piece(chars[char], "black", char))

            pieces.append(line)

        return pieces

    def render(self, filename: str):
        if filename in cache:
            return filename

        if Path(filename).exists():
            cache.add(filename)
            return filename

        board = Image.open("./static/board.png")

        for i in range(8):
            h = ""
            for j in range(8):
                p = self.b[i][j]
                if not p.name:
                    continue

                offset = ((64 * j), (64 * i))
                im = Image.open(p.filename)
                board.paste(im, offset, im)
                im.close()

        board.save("/data/" + filename)

        return filename
