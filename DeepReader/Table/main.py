import boto3
from botocore.exceptions import ClientError
s3 = boto3.resource('s3')
BUCKET_NAME = 'tabledependencies'
FOLDER='python'
try:
    local_file_name = '/tmp/python'
    s3.Bucket(BUCKET_NAME).download_file(FOLDER, local_file_name)
except ClientError as e:
    if e.response['Error']['Code'] != "404":
        raise


import pandas as pd
import subprocess 
import os
import sys
from handle_csv import convert_tsv_to_json
from data_transfer import upload_to_storage, download_from_storage
import shutil

from google.cloud import storage
client = storage.Client()
bucket_name = ''
bucket = client.get_bucket(bucket_name)

def download_file_from_gcs(source, dest):
    blob = bucket.blob(source)
    blob.download_to_filename(dest)

def upload_to_gcp_storage(source,dest):
    blob = bucket.blob(dest)
    blob.upload_from_filename(filename=source)

def run_table_process(image_path, cloud, temporary_folder, destination_folder, headers, log_string = "", use_gpu = True):
    log_string = log_string + "\nstarting the process"
    
    '''
    Writing all the headers 
    '''
    if not os.path.exists(temporary_folder):
        os.makedirs(temporary_folder)
    path_to_header_file = os.path.join(temporary_folder, "headers.csv")
    with open(path_to_header_file, "w") as f:
        f.write(",".join(headers))

    process = subprocess.Popen("sh sample.sh {} {}/ {}/ {} {}".format(image_path, temporary_folder, destination_folder, path_to_header_file, use_gpu), shell=True)
    process.wait()
    print("Sample.sh completed execution successfully")
    path_to_output_file = os.path.join(destination_folder, os.path.basename(image_path)[:-4] + "_generated_result.csv")
    
    if os.path.exists(path_to_output_file):
        log_string = log_string + "\noutput file created successfully"
        upload_to_storage(path_to_output_file, os.path.basename(image_path)[:-4] + "_generated_result.csv", cloud)
        json_read = convert_tsv_to_json(path_to_output_file)
        return log_string
    else:
        log_string = log_string + "\noutput file was not created"
        return log_string

def table_handler(request):    
    data = request.get_json()    
    image_name = data["image_name"]

    cloud="GCP"
    if "storage" in data:
        cloud = data["storage"]
    
    image_path = "/tmp/" + image_name
    download_from_storage(image_name,image_path, cloud)
    data["image_path"] = image_path

    log_string = ""
    index = 0
    use_gpu = False
    
    filename_only = image_name[:-4]
    path_to_server_data = "/tmp/server_dump"
    if not os.path.exists(path_to_server_data):
        os.mkdir(path_to_server_data)
    file_name_tb = str(filename_only) + "_textblock_master.json"
    path_to_file = os.path.join(path_to_server_data, file_name_tb )
    download_from_storage(file_name_tb,path_to_file,cloud)

    temporary_folder = os.path.join("/tmp/", "temporary_folder",image_name[:-4])
    destination_folder = os.path.join("/tmp/", "output_folder",image_name[:-4])
            
    if "temporary_folder" in data:
        temporary_folder = data["temporary_folder"]

    if "destination_folder" in data:
        destination_folder = data["destination_folder"]

    if not(os.path.exists(temporary_folder)):
        os.makedirs(temporary_folder)
            
    if not(os.path.exists(destination_folder)):
        os.makedirs(destination_folder)
    
    headers = ['carton', 'id', 'QTY', 'Description', 'UOM', 'Amount', 'Unit', 'Cost', 'Item', 'Price', 'Tax', 'quantity', 'serial']
    if "headers" in data:
        headers = data["headers"]
                        
    # This is the main function that we will run, it is expected to return a pandas dataframe
    log_string = run_table_process(image_path, cloud, temporary_folder, destination_folder, headers, log_string = log_string, use_gpu = use_gpu)

    os.remove(image_path)
    os.remove(path_to_file)
    shutil.rmtree(temporary_folder)
    shutil.rmtree(destination_folder)       

    return {'result' : "success",  "log" : log_string}
    