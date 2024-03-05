import os
import json

import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    # pre_authorization_token = event.get("chargeId")
    # customer_id = event.get("customerId")

    # if not pre_authorization_token:
    #     # metrics.add_metric(name="InvalidPaymentRequest", unit=MetricUnit.Count, value=1)
    #     # logger.error({"operation": "input_validation", "details": event})
    #     raise ValueError("Invalid Charge ID")

    # print(f"Refunding to from customer {customer_id} using {pre_authorization_token} token")
    print("Refunding payment...")

    responseF6 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F7-cancel-booking',
        InvocationType = 'Event'
        )