import csv
import MySQLdb
import boto3

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
    filename = f'week13-JeanDega.csv'  # Construct the filename using your desired value
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
        aws_access_key_id='AKIAQEIRHNZHHZVC5ACL',  # Replace with your actual AWS access key ID
        aws_secret_access_key='xxCnPFUSXZCjKwEVnvvdxLYkcFB/O86zcsitDFuH',  # Replace with your actual AWS secret access key
    )

    # Upload the CSV file to S3
    filename = f'week13-JeanDega.csv'  # Construct the filename using your desired value
    s3.upload_file(filename, 'UML', filename)  # Replace with your actual S3 bucket name
