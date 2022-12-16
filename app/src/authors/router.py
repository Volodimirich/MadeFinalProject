import ast
from typing import List
from collections import defaultdict
from fastapi import (
    Depends,
    APIRouter,
    Request,
)
from fastapi.templating import Jinja2Templates

from src.security import manager
from src.db import db
from src.auth.models import User
from src.papers.models import Paper
from src.authors.models import Author

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/authors", tags=["authors"], dependencies=[Depends(manager)])


# Sort APIs
@router.get(
    "/sort",
    response_description="Author cite top",
    response_model=List[Paper],
)
def author_sort(request: Request):
    pipeline = [{"$sort": {"n_citation": -1}}]
    author_dict = defaultdict(int)
    for paper in db.papers_collection.aggregate(pipeline=pipeline):
        amount = paper["n_citation"] if "n_citation" in paper else 0
        if "authors" in paper:
            for row in paper["authors"]:
                if "name" in row:
                    author_dict[row["name"]] += amount

    data = list(author_dict.items())
    data.sort(key=lambda x: x[1], reverse=True)
    for pos, element in enumerate(data):
        data[pos] = {"author": element[0], "citations": element[1]}
    return templates.TemplateResponse(
        "sort.html",
        {"request": request, "authors": data[:200]},
    )


@router.get("/recommendation_page")
def search_page(request: Request, _: User = Depends(manager)):
    return templates.TemplateResponse("recommendation_page.html", {"request": request})


@router.get(
    "/recommend",
    response_description="Recommend authors by another",
    response_model=List[Author],
)
def paper_search(
    request: Request,
    author: str = None,
):
    found_author: dict  # {'_id': '53f45ad4dabfaee1c0b3e206', 'name': 'Bonnie Mitchell'}
    ret = db.authors_collection.aggregate(
        pipeline=[
            {"$match": {"name": author}},
            # {"$match": {"name": {"$regex": f"^.*{author}.*$"}}},
        ]
    )
    try:
        found_author = next(ret)
    except StopIteration:
        return templates.TemplateResponse(
            "recommendation_page.html",
            {"request": request, "msg": f"Author '{author}' hasn't been found."},
        )

    # {'_id': '53f42cfedabfaee02ac5b495',
    # '0': "('53f561bedabfae5c2ef8045b', 0.816496580927726)"...
    recommend_authors: dict
    ret = db.author2author.aggregate(
        pipeline=[
            {"$match": {"_id": found_author["_id"]}},
        ]
    )
    try:
        recommend_authors_ret = next(ret)
    except StopIteration:
        return templates.TemplateResponse(
            "recommendation_page.html",
            {
                "request": request,
                "msg": f"Recommendations for '{author}' hasn't been found.",
            },
        )

    print(f"{found_author=}")

    recommend_authors: list = []

    for key, val in recommend_authors_ret.items():
        if key == "_id" or not val:
            continue
        print(f"{val=}")
        rec_id, confidence = ast.literal_eval(val)
        rec_name = db.authors_collection.find_one({"_id": rec_id})
        if rec_name is None:
            rec_name = f"unknown_{rec_id}"
        else:
            rec_name = rec_name["name"]
        recommend_authors.append((rec_name, confidence))

    print(f"{recommend_authors=}")

    return templates.TemplateResponse(
        "recommendation_result.html",
        {"request": request, "target_author": author, "authors": recommend_authors},
    )
