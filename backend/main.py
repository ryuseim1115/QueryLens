import os

from api.dependencies.require_login import NotLoggedInError
from api.routers import (
    create_table,
    drop_table,
    get_file_table_status,
    input,
    login,
    purge_file,
    register,
    result,
    result_view,
    run_query,
    upload_csv,
)
from config import SESSION_MAX_AGE_SECONDS, SESSION_SECRET_KEY, TEMPLATES_DIR
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from infrastructure.mysql import models
from infrastructure.mysql.user_db import engine
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    SessionMiddleware, secret_key=SESSION_SECRET_KEY, max_age=SESSION_MAX_AGE_SECONDS
)


# require_login_page(未ログインのページアクセス)が投げるNotLoggedInErrorを
# /loginへのリダイレクトに変換する。exception_handlerの登録はappを持つ
@app.exception_handler(NotLoggedInError)
def handle_not_logged_in(request: Request, exception: NotLoggedInError):
    return RedirectResponse(url="/login")


# サービス層はHTTPを知らないため、業務エラーはHTTPExceptionではなくValueErrorで
# 表現する。ここで一括してHTTPの語彙(400)に変換し、各ルータでのtry/exceptを不要にする
@app.exception_handler(ValueError)
def handle_value_error(request: Request, exception: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exception)})


models.Base.metadata.create_all(bind=engine)
js_path = os.path.join(TEMPLATES_DIR, "js")
css_path = os.path.join(TEMPLATES_DIR, "css")

app.mount("/js", StaticFiles(directory=js_path), name="js")
app.mount("/css", StaticFiles(directory=css_path), name="css")

app.include_router(register.router)
app.include_router(login.router)
app.include_router(input.router)
app.include_router(result.router)
app.include_router(result_view.router)
app.include_router(run_query.router)
app.include_router(upload_csv.router)
app.include_router(create_table.router)
app.include_router(drop_table.router)
app.include_router(purge_file.router)
app.include_router(get_file_table_status.router)
