import json
import os

import boto3
from botocore.exceptions import ClientError

# session = boto3.Session()
# dynamodb = session.resource('dynamodb')
# table = dynamodb.Table(os.environ['FLIGHT_TABLE_NAME'])

client = boto3.client('lambda')

def lambda_handler(event, context):
    F2_params = {
        'outboundFlightId': "5347fc8e-46f2-434d-9d09-fa4d31f7f266"
    }
    print("F1 - Start\n")
    # return {
    #     'statusCode': 200,
    #     # 'body': json.dumps('Hello from Lambda!')
    #     'body': client.invoke(
    #     FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F2-reserve-flight',
    #     InvocationType = 'Event',
    #     Payload = json.dumps(F2_params)
    #     )
    # }
    responseF1 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F2-reserve-flight',
        InvocationType = 'Event',
        Payload = json.dumps(F2_params)
        )
    return "yay"
