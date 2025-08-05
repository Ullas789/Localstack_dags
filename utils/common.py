from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import boto3
import logging
import os
from utils.exceptions import *
from utils.constants import *
from utils.s3_utils import *

def download_sql_from_s3(s3_key, bucket):
    """Download SQL file from S3 (LocalStack) and return local path."""
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT_URL'), 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
        region_name=os.getenv('AWS_REGION') 
    )
    local_tmp_dir = S3_LOCAL_TMP_DIR
    local_path = os.path.join(local_tmp_dir, s3_key)
    try:
        s3.download_file(bucket, s3_key, local_path)
        logging.info(f"Downloaded {s3_key} to {local_path}")
    except Exception as e:
        logging.error(f"Failed to download {s3_key}: {e}")
        raise SQLDownloadError("Failed to download SQL from S3") from e
    return local_path



def execute_sql_from_file(s3_key, conn_id):
    """
    Reads and executes an SQL file from the local temporary directory.

    Args:
        s3_key (str): The name of the SQL file.
        conn_id (str): The Airflow Postgres connection ID.

    Raises:
        Exception: If the SQL file cannot be read or executed.
    """
    try:
        # Get the local temporary directory from environment variables
        local_tmp_dir = os.getenv('S3_LOCAL_TMP_DIR', '/tmp')  # Default to '/tmp' if not set
        sql_file = os.path.join(local_tmp_dir, s3_key)

        logging.info(f"Reading SQL file from {sql_file}")

        # Check if the file exists
        if not os.path.exists(sql_file):
            raise FileNotFoundError(f"SQL file not found: {sql_file}")

        # Open and read the SQL file
        with open(sql_file, "r") as f:
            sql = f.read()

        # Execute the SQL using PostgresHook
        hook = PostgresHook(postgres_conn_id=conn_id)
        hook.run(sql)

        logging.info(f"Successfully executed SQL from {sql_file}")

    except Exception as e:
        logging.error(f"File not found: {e}")
        raise FileNotFoundError(f"SQL file not found: {sql_file}") from e
    except Exception as e:
        logging.error(f"Failed to execute SQL from {sql_file}: {e}")
        raise SQLExecutionError("Failed to execute SQL from file") from e


def create_dynamic_sql_dag(dag_id,variable):

    # variable=os.getenv('SQL_JOB_CONFIG_VAR'), 
    try:
        config = Variable.get(variable, deserialize_json=True)
    except Exception as r:
        raise VariableNotFoundError(f"Airflow Variable '{variable}' does not exist. Please add it in the Airflow UI or CLI.")


    with DAG(
        dag_id=dag_id,
        default_args={"start_date": datetime(2024, 1, 1)},
        schedule_interval=None,
        catchup=False
    ) as dag:
        
        previous_task = None

        for step in config["queries"]:
            s3_key = step["s3_path"]
            task_id = step["task_id"]

            download_task = PythonOperator(
                task_id=f"download_{task_id}",
                python_callable=download_sql_from_s3,
                op_kwargs={"s3_key": s3_key, "bucket": config["bucket"]},
            )

            run_task = PythonOperator(
                task_id=task_id,
                python_callable=execute_sql_from_file,
                op_kwargs={"s3_key": s3_key, "conn_id": config["database_connection_id"]},
            )

            if previous_task:
                previous_task >> download_task >> run_task
            else:
                download_task >> run_task

            previous_task = run_task

        return dag