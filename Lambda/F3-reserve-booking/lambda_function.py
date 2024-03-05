import datetime
import json
import os
import uuid

import boto3
from botocore.exceptions import ClientError

client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        booking_id = str(uuid.uuid4())
        state_machine_execution_id = event['name']
        outbound_flight_id = event['outboundFlightId']
        customer_id = event['customerId']
        payment_token = event['chargeId']
        seat_allotted = event['seat']
        
        print("Reserving Seat 12D on flight")
        booking_item = {
            "id": booking_id,
            "stateExecutionId": state_machine_execution_id,
            "__typename": "Booking",
            "bookingOutboundFlightId": outbound_flight_id,
            "seatAllotted": seat_allotted,
            "checkedIn": False,
            "customer": customer_id,
            "paymentToken": payment_token,
            "status": "UNCONFIRMED",
            "createdAt": str(datetime.datetime.now()),
        }
        # return booking_item
        
    except:
        print("Booking Error")
    # return "0"
    
    F4_params = {
        'name': "46dd7e36-fe5d-4823-ba46-c2c0663b2130",
        'chargeId': "ch_1EeqlbF4aIiftV70qXHQewmn",
        'customerId': "d749f277-0950-4ad6-ab04-98988721e475",
        'seat': event['seat'],
        'outboundFlightId': event['outboundFlightId']
    }
    responseF3 = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:F4-collect-payment',
        # FunctionName = 'arn:aws:lambda:us-east-1:299145856868:function:A2-dummy-node',
        InvocationType = 'Event',
        Payload = json.dumps(F4_params)
        )
