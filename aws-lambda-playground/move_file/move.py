import json
from datetime import datetime, timedelta
import boto3

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    """
    The Lambda function is operating on time basis, so no bucket event need to be created.

    run on schedule by using cron or rate expressions.
    """


    SOURCE_BUCKET = 'arn:aws:s3:::origin-bucket-test-1216'
    DESTINATION_BUCKET = 'bucket-b'

    s3_client = boto3.client('s3')


    paginator = s3_client.get_paginator('list_objects_v2')
    # Loop through each object, looking for ones older than a given time period
    now = datetime.now()
    current_time = now.strftime("%A, %d. %B %Y %I:%M%p")
    key_support = now.strftime("/%y/%m/%d/")
    for page in paginator:
        for object in page['Contents']:
            # the change happened in last 24 hours.
            if object['LastModified'] > datetime.now().astimezone() - timedelta(days=1):   # <-- Change time period here
                print(f"Moving {object['Key']}")

                # Copy object
                s3_client.copy_object(
                    Bucket=DESTINATION_BUCKET,
                    Key=key_support+object['Key'],
                    CopySource={'Bucket':SOURCE_BUCKET, 'Key':object['Key']}
                )

                # Delete original object
                s3_client.delete_object(Bucket=SOURCE_BUCKET, Key=object['Key'])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world?",
            "time":current_time,
            # "location": ip.text.replace("\n", "")
        }),
    }
