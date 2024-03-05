import json
import time

def lambda_handler(event, context):
    for i in range(1,180):
        print("yay")
        time.sleep(1)
    print("Done")