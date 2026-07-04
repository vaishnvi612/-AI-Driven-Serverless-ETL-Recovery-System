import boto3
from datetime import datetime

s3 = boto3.client("s3")
sns = boto3.client("sns")

FAILED_BUCKET = "yash-etl-failed-zone"

TOPIC_ARN = "arn:aws:sns:ap-south-1:258484763558:ETLAlerts"


def lambda_handler(event, context):

    # Read values safely
    bucket = event.get("bucket")
    key = event.get("key")

    if bucket and key:
        s3.copy_object(
            CopySource={
                "Bucket": bucket,
                "Key": key
            },
            Bucket=FAILED_BUCKET,
            Key=key
        )

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="❌ ETL Pipeline Failure",
        Message=f"""
AI-Driven Serverless ETL Recovery System

Status : FAILED

Dataset : {key}

Reason :
{event.get('reason','Validation / Glue Failure')}

Action Taken
✔ Recovery Lambda Executed
✔ File copied to Failed Bucket
✔ CloudWatch Logs Generated

Time :
{datetime.now()}
"""
    )

    return {
        "status": "RECOVERED"
    }