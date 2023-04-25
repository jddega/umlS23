from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import csv
import MySQLdb
import boto3

# Define default_args dictionary to specify default parameters of DAG, such as start date, frequency, etc.
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create a DAG instance and pass the default_args dictionary
dag = DAG(
    'upload_to_s3_dag',
    default_args=default_args,
    schedule_interval=timedelta(days=1),  # Change the frequency to your desired value
)

# Function to load data from MySQL and create a CSV file
def load_data_from_mysql_and_create_csv():
    # Connect to MySQL database
    conn = MySQLdb.connect(
        host='mysql',
        user='root',
        passwd='password',
        db='db',
    )
    cursor = conn.cursor()

    # Fetch data from MySQL table
    cursor.execute('SELECT * FROM Orders;')  # Change the query to your desired value
    data = cursor.fetchall()

    # Create a CSV file with the fetched data
    filename = f'week13-JeanDega.csv'  # Construct the filename using username
    with open(filename, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['OrderId', 'OrderStatus', 'LastUpdated'])  # Replace with your actual column names
        csv_writer.writerows(data)

    # Close MySQL cursor and connection
    cursor.close()
    conn.close()

# Function to write CSV file to S3
def write_csv_to_s3():
    # Create an S3 client
    s3 = boto3.client('s3',
        aws_access_key_id='AKIAQEIRHNZHHZVC5ACL',
        aws_secret_access_key='xxCnPFUSXZCjKwEVnvvdxLYkcFB/O86zcsitDFuH',
        region_name='us-east-1',  # Add the AWS region where your S3 bucket is located
    )

    # Upload the CSV file to S3
    filename = f'week13-JeanDega.csv'  # Construct the filename using username
    s3.upload_file(filename, 'UML', filename)

# Create two PythonOperator tasks, one for each function, that will be executed as part of the DAG
load_data_task = PythonOperator(
    task_id='load_data_from_mysql_and_create_csv',
    python_callable=load_data_from_mysql_and_create_csv,
    dag=dag,
)

write_csv_task = PythonOperator(
    task_id='write_csv_to_s3',
    python_callable=write_csv_to_s3,
    dag=dag,
)

# Set the task dependencies
load_data_task >> write_csv_task
