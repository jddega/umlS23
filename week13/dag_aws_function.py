import airflow
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s
import os

volume = k8s.V1Volume(
    name='test-volume',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='centos-pv-claim'),
)

volume_mount = k8s.V1VolumeMount(
    name='test-volume', mount_path='/root/mount_file', sub_path=None
)

default_args = {
    'owner': 'Jean Dega',
    'start_date': datetime(2023, 4, 22),
    'retries': 1,
}

dag = DAG('aws_python_script',
    default_args=default_args,
    schedule_interval='@once'
)

task1 = KubernetesPodOperator(
    task_id='run_script',
    name='myql_file',
    namespace='airflow',
    volumes=[volume],
    volume_mounts=[volume_mount],
    env_vars={
        'PYTHONPATH': '/root/mount_file',
        'MYSQL_CONN': '{{ var.value.MYSQL_CONN }}',
        'AWS_CONN': '{{ var.value.AWS_CONN }}'
    },
    image='dlambrig/week13:1.0',
    cmds=['python', '-c', 'from aws_function import my_function; my_function()'],
    arguments=[],
    dag=dag,
)

'''
task2 = KubernetesPodOperator(
    task_id='my_script',
    name='upload_aws',
    namespace='airflow',
    volumes=[volume],
    volume_mounts=[volume_mount],
    env_vars={
        'PYTHONPATH': '/root/mount_file',
        'AWS_CONN': '{{ var.value.AWS_CONN }}'
    
    image='dlambrig/week13:1.0',
    cmds=['python', '-c', 'from aws_function import upload_csv, upload_csv()'],
    arguments=[],
    dag=dag,
)

# set the task dependencies
task1 >> task2     
'''
