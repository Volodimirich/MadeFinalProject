from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.db import db

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["users"])


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    papers_count: int = db.papers_collection.count_documents({})
    users_count: int = db.users_collection.count_documents({})
    authors_count: int = db.authors_collection.count_documents({})

    return templates.TemplateResponse(
        "homepage.html",
        {
            "request": request,
            "papers_count": papers_count,
            "users_count": users_count,
            "authors_count": authors_count,
        },
    )


@router.get("/hello")
def get_hello():
    return {"message": "Hello!"}
