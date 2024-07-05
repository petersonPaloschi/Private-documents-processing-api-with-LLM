from fastapi import FastAPI, HTTPException, Request, status
from functions import  tokenizer_class
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):

    embed = tokenizer_class.EmbeddingProcessor()
    app.state.embed = embed
    app.state.chain = embed.create_chain("CDC")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    department = data.get("department").upper()
    query = data.get("query")


    if department == "CDC": 
        response = app.state.embed.get_response(query, app.state.chain)

    return response