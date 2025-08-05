# exceptions.py

class SQLDownloadError(Exception):
    """Raised when there is an error downloading SQL from S3."""
    pass

class SQLExecutionError(Exception):
    """Raised when there is an error executing SQL."""
    pass

class FileNotFoundError:
    """Raised when a file is not found."""
    pass

class VariableNotFoundError(Exception):
    """Raised when an Airflow Variable is not found."""
    pass
class CreateDAGError(Exception):
    """Raised when there is an error creating a DAG."""
    pass