import time
import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Try Again")
    time.sleep(60)
    count=int(event.get('count'))
    param = {
        'count':str(count+60)+""
    }
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:DummyNode1',
        InvocationType = 'Event',
        Payload = json.dumps(param)
        )