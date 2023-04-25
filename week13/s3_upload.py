import boto3
from auth import ACCESS_KEY, SECRET_KEY
from kubernetes.client import models as k8s
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime
from airflow import DAG


#ACCESS_KEY="AKIAQEIRHNZHHZVC5ACL"
#SECRET_KEY="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"

volume = k8s.V1Volume(
    name='test-volume',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='centos-pv-claim'),
)

volume_mount = k8s.V1VolumeMount(
    name='test-volume', mount_path='/root/mount_file', sub_path=None
)


def pushs3():
    client=boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    # client.create_bucket(Bucket='UML')
    with open("/root/tmp/data.csv", "rb") as f:
        client.upload_fileobj(f,"UML", "week13-JeanDega1.csv")
    
    print("uploaded completed")
    
