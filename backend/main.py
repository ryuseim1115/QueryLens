import os

from api.dependencies.require_login import NotLoggedInError
from api.routers import (
    analyze_query,
    create_table,
    drop_table,
    get_file_table_status,
    input,
    landing,
    login,
    logout,
    purge_file,
    register,
    result,
    result_view,
    run_query_block,
    upload_csv,
)
from config import TEMPLATES_DIR
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from infrastructure.mysql import models
from infrastructure.mysql.user_db import engine

app = FastAPI()


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
images_path = os.path.join(TEMPLATES_DIR, "images")

app.mount("/js", StaticFiles(directory=js_path), name="js")
app.mount("/css", StaticFiles(directory=css_path), name="css")
app.mount("/images", StaticFiles(directory=images_path), name="images")

app.include_router(landing.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(input.router)
app.include_router(result.router)
app.include_router(result_view.router)
app.include_router(analyze_query.router)
app.include_router(run_query_block.router)
app.include_router(upload_csv.router)
app.include_router(create_table.router)
app.include_router(drop_table.router)
app.include_router(purge_file.router)
app.include_router(get_file_table_status.router)
