import os
from typing import List
from bson import ObjectId
from fastapi import Body, FastAPI, Response, status, HTTPException, Request, Query
from pymongo import MongoClient, ReturnDocument
from models import Paper, UpdatePaper

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


# Create API
@app.post("/papers", status_code=status.HTTP_201_CREATED)
async def add_paper(request: Request, paper: Paper):
    result = request.app.database["dblpv13"].insert_one(paper.to_json())
    return request.app.database["dblpv13"].find_one({"_id": result.inserted_id})


# Read API
@app.get("/papers", response_description="List all papers", response_model=List[Paper])
async def list_papers(request: Request, limit: int = 100, page: int = 1):
    skip = (page - 1) * limit
    papers = list(request.app.database["dblpv13"].find(limit=limit, skip=skip))
    return papers


@app.get(
    "/papers/search",
    response_description="Search papers by title",
    response_model=List[Paper],
)
async def paper_search(
    request: Request,
    title: str = Query(default=None, min_length=3, max_length=50),
    limit: int = 100,
    page: int = 1,
):
    skip = (page - 1) * limit
    papers = list(
        request.app.database["dblpv13"].find(
            {"title": {"$regex": f"^.*{title}.*$"}}, limit=limit, skip=skip
        )
    )
    return papers


@app.get(
    "/papers/{paper_id}", response_description="Paper by paper_id", response_model=Paper
)
async def paper_by_id(request: Request, paper_id: str):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )

    paper = request.app.database["dblpv13"].find_one({"_id": paper_id})
    if paper is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found paper_id: {paper_id}",
        )

    return paper


# Update API
# TODO(besteady): make properly with existance check
@app.put(
    "/papers/{paper_id}", response_description="Update paper", response_model=Paper
)
async def update_paper_by_id(
    request: Request, paper_id: str, paper: UpdatePaper = Body(...)
):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )
    return request.app.database["dblpv13"].find_one_and_update(
        {"_id": paper_id},
        {"$set": paper.to_json()},
        return_document=ReturnDocument.AFTER,
    )


# Delete API
@app.delete("/papers/{paper_id}", response_description="Delete paper")
async def delete_paper_by_id(request: Request, paper_id: str):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )
    paper = request.app.database["dblpv13"].find_one_and_delete({"_id": paper_id})
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found paper_id: {paper_id}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
