# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from datetime import datetime
# import boto3




# def read_sql_file(file_path):
#     with open(file_path, "r") as f:
#         return f.read()
 
# def download_sql_from_s3(filename, bucket='my-sql-bucket'):
#     s3 = boto3.client(
#         's3',
#         endpoint_url='http://localstack:4566',  # internal network inside Docker
#         aws_access_key_id='test',
#         aws_secret_access_key='test',
#         region_name='us-east-1'
#     )
#     s3.download_file(bucket, filename, f'/tmp/{filename}')

# default_args = {
#     'start_date': datetime(2024, 1, 1),
# }

# with DAG(
#     dag_id='run_sql_from_s3',
#     schedule_interval=None,
#     default_args=default_args,
#     catchup=False,
# ) as dag:



#     download_create = PythonOperator(
#         task_id='download_create_table_sql',
#         python_callable=download_sql_from_s3,
#         op_kwargs={'filename': 'create_table.sql'},
#     )

#     run_create = PostgresOperator(
#         task_id='run_create_table',
#         postgres_conn_id='postgres_default',
#         sql=read_sql_file("/tmp/create_table.sql"),
#     )

#     download_insert = PythonOperator(
#         task_id='download_insert_sql',
#         python_callable=download_sql_from_s3,
#         op_kwargs={'filename': 'insert_data.sql'},
#     )
    

#     run_insert = PostgresOperator(
#         task_id='run_insert_sql',
#         postgres_conn_id='postgres_default',
#         sql=read_sql_file('/tmp/insert_data.sql'),
#     )
#     download_result = PythonOperator(
#         task_id='download_result_table_sql',
#         python_callable=download_sql_from_s3,
#         op_kwargs={'filename': 'result_table.sql'},
#     )
#     run_result_table= PostgresOperator(
#         task_id='run_result_table_sql',
#         postgres_conn_id='postgres_default',
#         sql=read_sql_file('/tmp/result_table.sql'),
#     )

#     download_avg = PythonOperator(
#         task_id='download_avg_sql',
#         python_callable=download_sql_from_s3,
#         op_kwargs={'filename': 'avg_salary.sql'},
#     )

#     run_avg = PostgresOperator(
#         task_id='run_avg_sql',
#         postgres_conn_id='postgres_default',
#         sql=read_sql_file('/tmp/avg_salary.sql'),
#     )

#     download_create  >> download_insert >> download_result  >> download_avg >> run_create >>run_insert >> run_result_table >>run_avg
