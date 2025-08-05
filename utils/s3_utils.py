import boto3
import os
from utils.constants import *
s3_config= boto3.client(
        's3',
        endpoint_url='http://localhost:4566', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
        region_name=os.getenv('AWS_REGION') 
    )
