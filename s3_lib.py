import logging
import boto3
from botocore.exceptions import ClientError

def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            bucket_response = s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            bucket_response = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        return bucket_response
    except ClientError as e:
        logging.error(e)
        return None

def add_file_to_bucket(bucket_name, file_name):
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket_name, file_name).upload_file(Filename=file_name)

bucket_name = 'test-bucket'
file_name = '.gitignore'
create_bucket(bucket_name)
add_file_to_bucket(bucket_name, file_name)