from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles

from os import environ as env
from hmac import compare_digest

from source.models import RenderRequest
from renderer.render import Board

app = FastAPI(docs_url=None)
app.mount("/data", StaticFiles(directory="/data"), name="data")

@app.post("/render")
async def render(data: RenderRequest, req: Request):
    if not compare_digest(req.headers.get("Authorization", ""), env["TOKEN"]):
        raise HTTPException(403)
    try:
        b = Board(data.fen)
    except:
        raise HTTPException(400, "Invalid FEN")

    name = data.fen.replace("/", "_") + ".png"
    url = "/data/" + b.render(name)

    return {"status":"ok", "url":url}