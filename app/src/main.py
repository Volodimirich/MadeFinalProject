from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from src.db import db
from src.auth.router import router as user_router
from src.papers.router import router as papers_router
from src.authors.router import router as authors_router
from src.base_router import router as base_router
from src.security import NotAuthenticatedException


app = FastAPI()
app.include_router(user_router)
app.include_router(papers_router)
app.include_router(authors_router)
app.include_router(base_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_db_client():
    db.define()


@app.on_event("shutdown")
def shutdown_db_client():
    db.close()


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, _: NotAuthenticatedException):
    return RedirectResponse(url="/auth/login")
