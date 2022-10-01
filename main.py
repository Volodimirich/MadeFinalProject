import os
from typing import List
from fastapi import FastAPI, Request
from pymongo import MongoClient
from models import Paper

app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(os.environ["MONGO_URI"])
    app.database = app.mongodb_client[os.environ["DB_NAME"]]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def index():
    return {"message": "Welcome To FastAPI World"}


@app.get("/papers", response_description="List all papers", response_model=List[Paper])
async def list_papers(request: Request):
    papers = list(request.app.database["dblpv13"].find(limit=100))
    return papers
