import boto3
from auth1 import ACCESS_KEY, SECRET_KEY



def pushs3():
    client=boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    #client.create_bucket(Bucket='UML')
    with open("/Users/jddeg/umlMsit5330Project/umlS23/week13/week13_JeanDega.csv", "rb") as f:
        client.upload_fileobj(f,"UML", "week13_JeanDega.csv")
    
    print("uploaded completed")
    
pushs3()
