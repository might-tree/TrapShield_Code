import os


# GCP Storage
from google.cloud import storage
gcp_st_client = storage.Client()
gcp_st_bucket_name = 'deep-reader'
gcp_st_bucket = gcp_st_client.get_bucket(gcp_st_bucket_name)

# AWS storage
import boto3
aws_service_Access_key = ''
aws_service_Secret = ''
aws_s3_client = boto3.client('s3', region_name='ap-south-1',
        aws_access_key_id=aws_service_Access_key,
        aws_secret_access_key=aws_service_Secret)
aws_s3_bucket_name="deep-reader-aws"


def download_from_gcp_storage(source,dest):
    gcp_st_blob = gcp_st_bucket.blob(source)
    gcp_st_blob.download_to_filename(dest)
  
def upload_to_gcp_storage(source,dest):
    gcp_st_blob = gcp_st_bucket.blob(dest)
    gcp_st_blob.upload_from_filename(filename=source)

def download_from_aws_s3(source,dest):
    aws_s3_client.download_file(aws_s3_bucket_name, source, dest)

def upload_to_aws_s3(source,dest):
    aws_s3_client.upload_file(source, aws_s3_bucket_name, dest)

    
def upload_to_storage(source, dest, cloud):
    if (cloud=="AWS"):
        upload_to_aws_s3(source,dest)
    elif (cloud=="GCP"):
        upload_to_gcp_storage(source,dest)
    else: 
        print("invalid storage service, so using aws")
        upload_to_aws_s3(source,dest)

def download_from_storage(source, dest, cloud):
    if (cloud=="AWS"):
        download_from_aws_s3(source,dest)
    elif (cloud=="GCP"):
        download_from_gcp_storage(source,dest)
    else: 
        print("invalid storage service, so using aws")
        download_from_aws_s3(source,dest)


