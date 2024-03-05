import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Notifying: Booking Failed")
    responseF9 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F10-booking-dlq',
        InvocationType = 'Event'
        )
