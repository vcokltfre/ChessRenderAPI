from pydantic import BaseModel


class RenderRequest(BaseModel):
    fen: str
