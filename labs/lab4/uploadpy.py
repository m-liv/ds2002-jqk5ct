#!/Users/miyad/.local/share/virtualenvs/DSS-R3gwlmMO/bin/python3
import requests
import os
import sys
import boto3

# Helper function to download a file using requests
def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded to {file_path}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading: {e}")

image_url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExcnRoZmJvdmRydjg5YW0xb2I0ZDB5MGxja3YxZmIzenVsdjl5aWdqMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/v6aOjy0Qo1fIA/giphy.gif"

# Command line arguments
object_name = sys.argv[1]
bucket_name = sys.argv[2]
expires_in = sys.argv[3]

# Download the file with the name object_name
path = os.path.join(os.getcwd(), object_name)
download_file(image_url, path)

# Upload the file to S3 bucket with the name object_name
s3 = boto3.client('s3')
# Using upload_file (learned in class) instead of put_object (in lab writeup) in order to
#   get the correct behavior with gif uploads.
response = s3.upload_file(object_name, bucket_name, object_name)

# Set presign to specified expiration seconds
response = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': bucket_name, 'Key': object_name},
    ExpiresIn=expires_in
)

# Print the presigned URL
print(response)