import boto3

BUCKET_NAME = "data-getaround-2026"

LOCAL_FILE = "data/outputs/analytics_bundle.json"

S3_KEY = "outputs/analytics_bundle.json"

s3 = boto3.client("s3")

s3.upload_file(
    Filename=LOCAL_FILE,
    Bucket=BUCKET_NAME,
    Key=S3_KEY
)

print(
    f"Uploaded s3://{BUCKET_NAME}/{S3_KEY}"
)