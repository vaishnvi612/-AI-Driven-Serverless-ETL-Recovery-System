import boto3
from datetime import datetime

sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:ap-south-1:258484763558:ETLAlerts"

def lambda_handler(event, context):

    dataset = event.get("key", "Unknown Dataset")

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="✅ ETL Pipeline Completed Successfully",
        Message=f"""
AI-Driven Serverless ETL Recovery System

Status : SUCCESS

Dataset : {dataset}

AI Prediction :
Healthy Dataset

Glue Job :
Completed Successfully

Output :
Processed S3 Bucket

Execution Time :
{datetime.now()}

Pipeline Completed Successfully.
"""
    )

    return {
        "status": "SUCCESS_EMAIL_SENT"
    }