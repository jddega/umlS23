from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from s3_upload1 import pushs3




default_args = {
    'owner': 'Jean Dega',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 22),
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

with DAG("S3_UPLOAD", default_args = default_args, schedule_interval="@daily", catchup=False) as dag:
    t1 = PythonOperator(task_id="s3-using-python", python_callable=pushs3)