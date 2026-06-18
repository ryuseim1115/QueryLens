import os

from api.routers import create_table, drop_table, get_csv_files, input, result, run_query, upload_csv
from config import TEMPLATES_DIR
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
static_path = os.path.join(TEMPLATES_DIR, "js")
css_path = os.path.join(TEMPLATES_DIR, "css")

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/css", StaticFiles(directory=css_path), name="css")

app.include_router(run_query.router)
app.include_router(get_csv_files.router)
app.include_router(input.router)
app.include_router(result.router)
app.include_router(upload_csv.router)
app.include_router(create_table.router)
app.include_router(drop_table.router)


