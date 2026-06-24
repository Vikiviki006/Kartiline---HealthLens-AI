"""
Storage client — local disk or S3 based on STORAGE_BACKEND config.
"""

from app.core.config import settings
from app.utils.logger import logger


def upload_to_s3(file_bytes: bytes, key: str) -> str:
    """Upload bytes to S3 and return the object URL."""
    import boto3

    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=file_bytes)
    url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
    logger.info(f"Uploaded to S3: {url}")
    return url


def get_storage_url(path: str) -> str:
    """Return the public URL for a stored file."""
    if settings.STORAGE_BACKEND == "s3":
        return f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{path}"
    return path
