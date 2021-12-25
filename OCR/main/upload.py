import boto3
from botocore.exceptions import NoCredentialsError
from config import ACCESS_KEY,SECRET_KEY
from PIL import Image
import os

bucket = 'ankitasuman-bucket'
filename = "images"
s3_filename = 's3_image'
s3_resource = boto3.resource("s3", region_name="us-east-2")



def upload_to_aws(local_file, bucket, s3_file):
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    # enumerate local files recursively
    for root, dirs, files in os.walk(local_file):

        for file in files:

            # construct the full local path
            local_path = os.path.join(root, file)

            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_file)
            s3_path = os.path.join(s3_file, relative_path)

            # relative_path = os.path.relpath(os.path.join(root, filename))

            print('Searching "%s" in "%s"' % (s3_path, bucket))
            try:
                client.head_object(Bucket=bucket, Key=s3_path)
                print("Path found on S3! Skipping %s..." % s3_path)

            # try:
                # client.delete_object(Bucket=bucket, Key=s3_path)
            # except:
                # print "Unable to delete %s..." % s3_path
            except:
                print("Uploading %s..." % s3_path)
                client.upload_file(local_path, bucket, s3_path)



# def uploadDirectory(path, bucketname, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
#     for root,dirs,files in os.walk(path):
#         for file in files:
#             s3.upload_file(os.path.join(root,file),bucketname, s3_file)


uploaded = upload_to_aws(filename, bucket, s3_filename)
