import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    # return("Collecting Payment...")
    print("Attacked!")
    param = {
        'count': "1"
    }
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:DummyNode1',
        InvocationType = 'Event',
        Payload=json.dumps(param)
        )