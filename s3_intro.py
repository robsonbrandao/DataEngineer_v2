import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Create an S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

# Listar buckets
response = s3.list_buckets()
for bucket in response["Buckets"]:
    print(f"Bucket Name: {bucket['Name']}")


# Escrever em um bucket 1
# bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
# object_name = "teste.txt"
# content = "Hello World!"
# s3.put_object(Bucket=bucket_name, Key=object_name, Body=content)


# Escrever em um bucket 2
bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
object_name = "posts.csv"

s3.put_object(Bucket=bucket_name, Key=object_name)


# Upload the file


s3.upload_file("posts.csv", bucket_name, object_name)
