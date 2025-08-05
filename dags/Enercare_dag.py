# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from airflow.models import Variable
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from datetime import datetime
# import boto3
# import logging

# def download_sql_from_s3(s3_key, bucket):
#     s3 = boto3.client(
#         's3',
#         endpoint_url='http://localstack:4566',
#         aws_access_key_id='test',
#         aws_secret_access_key='test',
#         region_name='us-east-1'
#     )
#     local_path = f"/tmp/{s3_key}"
#     try:
#         s3.download_file(bucket, s3_key, local_path)
#         logging.info(f"Downloaded {s3_key} to {local_path}")
#     except Exception as e:
#         logging.error(f"Failed to download {s3_key}: {e}")
#         raise
#     return local_path

# def execute_sql_from_file(s3_key, conn_id):
#     sql_file = f"/tmp/{s3_key}"
#     logging.info(f"Reading and executing SQL from {sql_file}")
#     with open(sql_file, "r") as f:
#         sql = f.read()

#     hook = PostgresHook(postgres_conn_id=conn_id)
#     hook.run(sql)
#     logging.info(f"Executed SQL from {sql_file}")

# def create_dynamic_sql_dag():
#     config = Variable.get("ENERCARE_CONFIG", deserialize_json=True)

#     with DAG(
#         dag_id="enercare_dag",
#         default_args={"start_date": datetime(2024, 1, 1)},
#         schedule_interval=None,
#         catchup=False
#     ) as dag:
        
#         previous_task = None

#         for step in config["queries"]:
#             s3_key = step["s3_path"]
#             task_id = step["task_id"]

#             download_task = PythonOperator(
#                 task_id=f"download_{task_id}",
#                 python_callable=download_sql_from_s3,
#                 op_kwargs={"s3_key": s3_key, "bucket": config["bucket"]},
#             )

#             run_task = PythonOperator(
#                 task_id=task_id,
#                 python_callable=execute_sql_from_file,
#                 op_kwargs={"s3_key": s3_key, "conn_id": config["database_connection_id"]},
#             )

#             if previous_task:
#                 previous_task >> download_task >> run_task
#             else:
#                 download_task >> run_task

#             previous_task = run_task

#         return dag

# globals()["dynamic_sql_runner"] = create_dynamic_sql_dag()





# from utils.common import create_dynamic_sql_dag
# import os

# variable=os.getenv('ENERCARE_CONFIG_VAR')
# globals()["enercare_dag"] = create_dynamic_sql_dag('enercare_dag',variable) 

# from utils.common import create_dynamic_sql_dag
# import os
# import logging

# def safe_create_dag(dag_id, env_var_name):
#     """Create a DAG only if env var & Airflow Variable are set."""
#     variable_name = os.getenv(env_var_name)
#     if not variable_name:
#         logging.warning(f"Env var {env_var_name} not set — skipping DAG {dag_id}")
#         return None
#     try:
#         return create_dynamic_sql_dag(dag_id, variable_name)
#     except Exception as e:
#         logging.error(f"Failed to create DAG {dag_id}: {e}")
#         return None

# # Create Enercare DAG
# enercare_dag = safe_create_dag('enercare_dag', 'ENERCARE_CONFIG_VAR')
# if enercare_dag:
#     globals()['enercare_dag'] = enercare_dag

# # Create Dynamic SQL Runner DAG
# dynamic_sql_dag = safe_create_dag('dynamic_sql_runner', 'SQL_JOB_CONFIG_VAR')
# if dynamic_sql_dag:
#     globals()['dynamic_sql_runner'] = dynamic_sql_dag
