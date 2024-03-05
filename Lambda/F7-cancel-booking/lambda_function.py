import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Booking Cancelled")
    responseF7 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F8-release-flight-seat',
        InvocationType = 'Event'
        )
