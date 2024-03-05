import json
import boto3
import time
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    print("Booking Failed")
    time.sleep(60)
    count=int(event.get('count'))
    param = {
        'count':str(count+60)+""
    }
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:DummyNode3',
        InvocationType = 'Event',
        Payload = json.dumps(param)
        )