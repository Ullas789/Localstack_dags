import os
import boto3
from utils.exceptions import *
from utils.constants import *  # Import the queries list
from utils.s3_utils import *
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
s3 = s3_config
bucket_name = s3_bucket_name
# Create bucket
s3.create_bucket(Bucket=bucket_name)

# Path to the SQL folder
sql_folder = sql_folder

# Upload SQL files
for filename in queries:
    file_path = os.path.join(sql_folder, filename)
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, filename)
        print(f"Uploaded {filename} from {file_path}")