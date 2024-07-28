if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from os import path
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError

@custom
def transform_custom(data):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
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
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=evidently_report)
        print(f"File uploaded successfully to {bucket_name}/{object_key}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Authentication failed")
    except Exception as e:  
        print(f"An error occurred: {e}")
    
    print(f'This is the type: {type(evidently_report)}')
    return evidently_report


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'