import boto3
import os

s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

bucket_name = 'my-sql-bucket'

# Create bucket
s3.create_bucket(Bucket=bucket_name)

# Path to the SQL folder
sql_folder = './sql_files'

# Upload SQL files
for filename in  ['create_table.sql', 'insert_data.sql', 'avg_salary.sql','result_table.sql']:
    file_path = os.path.join(sql_folder, filename)
    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, filename)
        print(f"Uploaded {filename} from {file_path}")