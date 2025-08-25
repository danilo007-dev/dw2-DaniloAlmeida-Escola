# app.py
# FastAPI application entry point

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API Escola rodando!"}
