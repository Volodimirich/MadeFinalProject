from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from src.auth.models import User
from src.db import db
from src.security import manager


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/auth", tags=["users"])


@manager.user_loader()
def load_user(username: str):
    users_col: Collection = db.users_collection
    user = users_col.find_one({"username": username})
    return user


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login_page.html", {"request": request})


@router.post("/login")
def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password

    user = load_user(username)
    if not user or password != user["password"]:
        return templates.TemplateResponse(
            "login_page.html",
            {
                "request": request,
                "errors": ["Invalid credentials"],
            },
        )

    access_token = manager.create_access_token(data=dict(sub=username))
    response = templates.TemplateResponse(
        "login_page.html",
        {
            "request": request,
            "msg": f"Success login: {access_token=}, token_type=bearer",
        },
    )
    manager.set_cookie(response, access_token)
    return response


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register_page.html", {"request": request})


@router.post("/register")
async def register(request: Request):
    user_col: Collection = db.users_collection
    form = await request.form()
    user = User(username=form.get("username"), password=form.get("password"))

    try:
        result = user_col.insert_one(user.to_json())
    except DuplicateKeyError:
        return templates.TemplateResponse(
            "register_page.html",
            {
                "request": request,
                "errors": ["A user with this username already exists"],
            },
        )

    assert user_col.find_one({"_id": result.inserted_id})
    return templates.TemplateResponse(
        "register_page.html", {"request": request, "msg": "User success added"}
    )
