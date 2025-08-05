from utils.common import create_dynamic_sql_dag
import os
import logging
from utils.exceptions import *


def create_dag(dag_id, env_var_name):
    """Create a DAG only if env var & Airflow Variable are set."""
    variable_name = os.getenv(env_var_name)
    if not variable_name:
        logging.warning(f"Env var {env_var_name} not set — skipping DAG {dag_id}")
        return None
    try:
        return create_dynamic_sql_dag(dag_id, variable_name)
    except Exception as e:
        logging.error(f"Failed to create DAG {dag_id}: {e}")
        raise CreateDAGError(f"Failed to create DAG {dag_id}: {e}") from e

# Create Enercare DAG
enercare_dag = create_dag('enercare_dag', 'ENERCARE_CONFIG_VAR')
if enercare_dag:
    globals()['enercare_dag'] = enercare_dag

# Create Dynamic SQL Runner DAG
dynamic_sql_dag = create_dag('dynamic_sql_runner', 'SQL_JOB_CONFIG_VAR')
if dynamic_sql_dag:
    globals()['dynamic_sql_runner'] = dynamic_sql_dag