import json
import boto3


BUCKET_NAME = "data-getaround-2026"

KEY = "outputs/analytics_bundle.json"


def load_analytics_bundle():

    s3 = boto3.client("s3")

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=KEY
    )

    data = json.loads(
        response["Body"].read()
    )

    return data