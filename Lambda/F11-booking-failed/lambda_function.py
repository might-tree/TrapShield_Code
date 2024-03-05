import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Booking Failed")
    responseF11 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F14-end',
        InvocationType = 'Event'
        )
