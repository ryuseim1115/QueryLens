import boto3
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY_ID,
    REGION_NAME,
    S3_BUCKET_NAME,
)


def delete_csv(file_name: str) -> None:
    client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
        region_name=REGION_NAME,
    )
    client.delete_object(Bucket=S3_BUCKET_NAME, Key=file_name)
