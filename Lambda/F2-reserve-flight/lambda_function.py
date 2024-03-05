import json
import os
import random

import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    
    if 'outboundFlightId' not in event:
        raise ValueError('Invalid arguments')
    rows = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    seats = ['A','B','C','D','E','F']
    
    print("Reserving seat 1B on flight")
    seat = str(random.choice(rows))+""+str(random.choice(seats))
    
    F3_params = {
        'name': "46dd7e36-fe5d-4823-ba46-c2c0663b2130",
        'chargeId': "ch_1EeqlbF4aIiftV70qXHQewmn",
        'customerId': "d749f277-0950-4ad6-ab04-98988721e475",
        'seat': seat,
        'outboundFlightId': event['outboundFlightId']
    }
    responseF2 = client.invoke(
        # FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F3-reserve-booking',
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:A1-dummy-node',
        InvocationType = 'Event',
        Payload = json.dumps(F3_params)
        )
    # responseF3 = json.load(responseF1['Payload'])
    # print(responseF3)
    
    # return flightDetails
