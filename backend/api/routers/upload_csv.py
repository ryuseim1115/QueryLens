import csv

import boto3
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY_ID,
    REGION_NAME,
    S3_BUCKET_NAME,
)
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from api.dependencies.require_login import require_login_api

router = APIRouter()


@router.post("/upload-csv", status_code=204)
def upload_csv(file: UploadFile = File(...), user_id: int = Depends(require_login_api)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename} はCSVファイルではありません。",
        )

    content = file.file.read()
    try:
        text = content.decode("utf-8")
        csv.Sniffer().sniff(text[:1024])
    except UnicodeDecodeError, csv.Error:
        raise HTTPException(
            status_code=400,
            detail=f"{file.filename} はCSV形式ではありません。",
        )

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
        region_name=REGION_NAME,
    )
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=f"{user_id}/{file.filename}", Body=content)
