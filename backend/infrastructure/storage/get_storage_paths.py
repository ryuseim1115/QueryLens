import boto3
from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY_ID,
    REGION_NAME,
    S3_BUCKET_NAME,
)


def get_storage_paths(user_id: int) -> list[str]:
    client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
        region_name=REGION_NAME,
    )
    files_info = client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f"{user_id}/")
    return [
        f"s3://{S3_BUCKET_NAME}/{file_info['Key']}"
        for file_info in files_info.get("Contents", [])
    ]
