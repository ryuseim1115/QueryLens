import os

from api.routers import (
    auth,
    create_table,
    delete_csv,
    drop_table,
    get_csv_files,
    input,
    login,
    register,
    result,
    result_view,
    run_query,
    upload_csv,
)
from config import SESSION_SECRET_KEY, TEMPLATES_DIR
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from infrastructure.mysql import models
from infrastructure.mysql.user_db import engine
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

models.Base.metadata.create_all(bind=engine)
js_path = os.path.join(TEMPLATES_DIR, "js")
css_path = os.path.join(TEMPLATES_DIR, "css")

app.mount("/js", StaticFiles(directory=js_path), name="js")
app.mount("/css", StaticFiles(directory=css_path), name="css")

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(run_query.router)
app.include_router(get_csv_files.router)
app.include_router(input.router)
app.include_router(result.router)
app.include_router(result_view.router)
app.include_router(upload_csv.router)
app.include_router(create_table.router)
app.include_router(drop_table.router)
app.include_router(delete_csv.router)
