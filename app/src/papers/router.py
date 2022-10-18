from typing import List
from bson import ObjectId
from fastapi import (
    Body,
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Request,
)
from fastapi.templating import Jinja2Templates
from pymongo import ReturnDocument

from src.security import manager
from src.db import db
from src.auth.models import User
from src.papers.models import Paper, UpdatePaper
from src.utils import PrettyJSONResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/papers", tags=["papers"], dependencies=[Depends(manager)])


@router.get("/search_page")
def search_page(request: Request, _: User = Depends(manager)):
    return templates.TemplateResponse("search_page.html", {"request": request})


# Papers API
# Create API
@router.post("", status_code=status.HTTP_201_CREATED)
def add_paper(paper: Paper):
    result = db.papers_collection.insert_one(paper.to_json())
    return db.papers_collection.find_one({"_id": result.inserted_id})


# Read API
@router.get("", response_description="List all papers", response_model=List[Paper])
def list_papers(limit: int = 100, page: int = 1):
    skip = (page - 1) * limit
    papers = list(db.papers_collection.find(limit=limit, skip=skip))
    return papers


# Search APIs


@router.get(
    "/search",
    response_description="Search papers by title/year/author/venue",
    response_model=List[Paper],
)
def paper_search(
    request: Request,
    title: str = None,
    year: str = None,
    author: str = None,
    venue: str = None,
    limit: int = 100,
    page: int = 1,
):
    skip = (page - 1) * limit

    search_query = {}
    if title:
        search_query["title"] = {"$regex": f"^.*{title}.*$"}
    if year:
        search_query["year"] = int(year)
    if author:
        search_query["authors.name"] = {"$regex": f"^.*{author}.*$"}
    if venue:
        search_query["venue.raw"] = {"$regex": f"^.*{venue}.*$"}

    papers = list(db.papers_collection.find(search_query, limit=limit, skip=skip))
    return templates.TemplateResponse(
        "papers_page.html", {"request": request, "papers": papers}
    )


@router.get(
    "/{paper_id}",
    response_description="Paper by paper_id",
    response_model=Paper,
    response_class=PrettyJSONResponse,
)
def paper_by_id(paper_id: str):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )

    paper = db.papers_collection.find_one({"_id": paper_id})
    if paper is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found paper_id: {paper_id}",
        )

    return paper


# Update API
# TODO(besteady): make properly with existance check
@router.put("/{paper_id}", response_description="Update paper", response_model=Paper)
def update_paper_by_id(paper_id: str, paper: UpdatePaper = Body(...)):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )
    return db.papers_collection.find_one_and_update(
        {"_id": paper_id},
        {"$set": paper.to_json()},
        return_document=ReturnDocument.AFTER,
    )


# Delete API
@router.delete("/{paper_id}", response_description="Delete paper")
def delete_paper_by_id(paper_id: str):
    if not ObjectId.is_valid(paper_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid paper_id: {paper_id}",
        )
    paper = db.papers_collection.find_one_and_delete({"_id": paper_id})
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found paper_id: {paper_id}",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
