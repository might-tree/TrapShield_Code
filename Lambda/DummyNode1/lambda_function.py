import json
import boto3
import time
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    # return("Stop")
    count=int(event.get('count'))
    print("Process Failed"+str(count))
    time.sleep(60)
    if count >= 180:
        return("Failed")
    param = {
        'count':str(count+60)+""
    }
    client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:DummyNode2',
        InvocationType = 'Event',
        Payload = json.dumps(param)
        )