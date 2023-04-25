from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define your default_args and other DAG parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance with a unique DAG ID
dag = DAG(
    'my_dag_id_aws',  # Update to a unique DAG ID, e.g. 'my_dag_id_aws'
    default_args=default_args,
    schedule_interval='@daily',  # Define your desired schedule interval
)

# Define your tasks as PythonOperator instances
def my_function():
    # Your task logic here
    pass

task1 = PythonOperator(
    task_id='task1',
    python_callable=my_function,
    dag=dag
)

task2 = PythonOperator(
    task_id='task2',
    python_callable=my_function,
    dag=dag
)

# Set task dependencies if needed
task1 >> task2
