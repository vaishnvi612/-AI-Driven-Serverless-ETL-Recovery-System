import boto3
import csv

s3 = boto3.client('s3')

def lambda_handler(event, context):

    bucket = event['bucket']
    key = event['key']

    obj = s3.get_object(Bucket=bucket, Key=key)

    content = obj['Body'].read().decode('utf-8')

    reader = csv.DictReader(content.splitlines())

    for row in reader:

        if (
            not row.get("id") or
            not row.get("name") or
            not row.get("salary")
        ):
            return {
                "status": "FAILED",
                "bucket": bucket,
                "key": key,
                "reason": "Missing mandatory fields"
            }

        try:
            salary = int(row["salary"])
            if salary < 0:
                return {
                    "status": "FAILED",
                    "bucket": bucket,
                    "key": key,
                    "reason": "Negative salary"
                }
        except:
            return {
                "status": "FAILED",
                "bucket": bucket,
                "key": key,
                "reason": "Invalid salary"
            }

    return {
        "status": "SUCCESS",
        "bucket": bucket,
        "key": key
    }