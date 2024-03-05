# curl -v -X POST       'https://ivxnx4ghivwmztlqffymnd4wpi0pdrdj.lambda-url.us-east-1.on.aws/'       -H 'content-type: application/json'       -d '{ "customerId": "d749f277-0950-4ad6-ab04-98988721e475", "chargeId": "ch_1Edea2F4aIiftV70kgOJC7FO" }'


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

    print(f"Collecting payment of $51...")
    ret = {
        'PaymentStatus' : "SUCCESS",
        'ConfirmBooking' : "YES",
        'bookingId' : "5347fc8e-46f2-434d-9d09-fa4d31f7f266"
    }
    
    F5_params = ret
    responseF4 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F5-confirm-booking',
        InvocationType = 'Event',
        Payload = json.dumps(F5_params)
        )
    # responseF4 = client.invoke(
    #     FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F9-notify-booking-failed',
    #     InvocationType = 'Event',
    #     # Payload = json.dumps(F5_params)
    #     )
