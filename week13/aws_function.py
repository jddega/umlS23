import os
import json
import pymysql
import csv
import boto3

def my_function():
    
    for key, value in os.environ.items():
        print(f"{key}: {value}")
    mysql_conn = os.environ.get("MYSQL_CONN")
    json_dict = json.loads(mysql_conn)
    user = json_dict["login"]
    pw = json_dict["password"]
    host = json_dict["host"]
    db = json_dict["database"]
    port = int(json_dict["port"])
    local_filename = "/root/mount_file/week13-JeanDega.csv"
    try:
        conn = pymysql.connect(host=host,user=user,password=pw,db=db,port=port)
        m_query = """SELECT * FROM Orders;"""
        m_cursor = conn.cursor()
        m_cursor.execute(m_query)
        results = m_cursor.fetchall()

        with open(local_filename, 'w') as fp:
            csv_w = csv.writer(fp, delimiter='|')
            csv_w.writerows(results)
            print(results)
    
        m_cursor.close()
        conn.close()
    except Exception as e:
        print(e)
    aws_conn = os.environ.get("AWS_CONN")
    json_dict = json.loads(aws_conn)
    user = json_dict['ACCESS_SECRET']
    pw = json_dict['ACCESS_KEY']
    s3 = boto3.client('s3', aws_access_key_id=pw, aws_secret_access_key=user)
    s3_file = "week13-JeanDega.csv" #*same as local_filename in try block"
    s3.upload_file(local_filename, 'UML', s3_file)