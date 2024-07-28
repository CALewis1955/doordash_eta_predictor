from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from pandas import DataFrame
from os import path
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_report_to_s3(html, **kwargs) -> None:
    """
    Template for exporting data to a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#s3
    """
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
    
    
    filepath = f'./mage_data/evidently_report_{datetime.now().strftime("%m-%d-%Y")}.html'   
    
    bucket_name = 'mlflow-clewis916-remote'
    object_key = f'evidently_report_{datetime.now().strftime("%m-%d-%Y")}'
    with open(filepath, 'r', encoding='utf-8') as file:
        evidently_report = file.read()

    # Initialize the S3 client
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)                         
    
    try:
    # Upload the file to S3
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=evidently_report, ContentType='text/html')
        print(f"File uploaded successfully to {bucket_name}/{object_key}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Authentication failed")
    
    return evidently_report