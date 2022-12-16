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
from src.tags_predict.tags2string import tags2string
from collections import Counter
import statistics

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/papers", tags=["papers"], dependencies=[Depends(manager)])


@router.get("/search_page")
def search_page(request: Request, _: User = Depends(manager)):
    return templates.TemplateResponse(
        "search_page.html", {"request": request, "tags": tags2string}
    )


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


# Get statistic
@router.get(
    "/statistic",
    response_description="Data statistic",
    response_model=List[Paper],
)
def data_statistic(request: Request):
    pipeline = [{"$sort": {"n_citation": -1}}]
    citations_values = []
    year_values = []
    top_fos = Counter()
    for paper in db.papers_collection.aggregate(pipeline=pipeline):
        if "n_citation" in paper:
            citations_values.append(paper["n_citation"])
        else:
            citations_values.append(0)

        if "year" in paper:
            year_values.append(paper["year"])

        if "fos" in paper:
            top_fos += Counter(paper["fos"])

    data = [
        {"text": "Citation mean value", "value": statistics.mean(citations_values)},
        {"text": "Citation median value", "value": statistics.median(citations_values)},
        {"text": "Year mean value", "value": statistics.mean(year_values)},
        {"text": "Year median value", "value": statistics.median(year_values)},
        {"text": "FOS most common word", "value": top_fos.most_common()[0][0]},
        {
            "text": "Amount of top common word usage",
            "value": top_fos.most_common()[0][1],
        },
    ]
    return templates.TemplateResponse(
        "statistic.html",
        {"request": request, "papers": data},
    )


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
    tag: str = None,
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

    pipeline = [
        {"$match": search_query},
        {
            "$lookup": {
                "from": "tags",
                "localField": "_id",
                "foreignField": "_id",
                "as": "my_tag",
            }
        },
        # {"$unwind": "$my_tag"},
        {"$project": {"my_tag._id": 0, "my_tag.row_num": 0}},
    ]

    if tag:
        pipeline.append({"$match": {"my_tag.label": f"[{tag}]"}})

    pipeline.extend([{"$skip": skip}, {"$limit": limit}])
    papers = []
    for paper in db.papers_collection.aggregate(pipeline=pipeline):
        val = paper["my_tag"]
        if val:
            my_label = val[0]["label"].strip("][")  # [{"label" : "[12]"}] -> "12"
            paper["my_tag"] = {"label": tags2string[my_label]}
        else:
            paper["my_tag"] = {"label": "None"}

        papers.append(paper)

    return templates.TemplateResponse(
        "papers_page.html",
        {"request": request, "papers": papers},
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
