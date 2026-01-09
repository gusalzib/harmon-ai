# Authors of code:
# - Viktor Kolak

from google.cloud import storage
import re
import os
import zipfile


def upload_blob_from_string(bucket_name, string_data, destination_blob_name, content_type='text/html'):
    """Uploads a string to the bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        string_data (str): The string content to upload.
        destination_blob_name (str): The destination path within the bucket.
        content_type (str): The content type of the blob, e.g., 'text/html'.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(string_data, content_type=content_type)

    print(f"String data uploaded to {destination_blob_name}.")

 
def upload_blob_from_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket.
    Args:
        bucket_name (str): The name of the GCS bucket.
        source_file_name (str): The path to the local file.
        destination_blob_name (str): The destination path within the bucket.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    

def get_all_reports(bucket_name,path_to_reports):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    reports = []
    #itarate through the folder/bucket with the path to the reports
    for blob in bucket.list_blobs(prefix=path_to_reports):
        if blob.name.endswith('/'):
            continue
        #save the version for request response format
        match = re.search(r'_v(\d+)', blob.name)
        version = int(match.group(1)) if match else None
        if version is None:
            print(f"Warning: No version found in {blob.name}")
        #append the reports to the response
        reports.append({
            "url": blob.public_url,
            "version": version,
            "name": "HarmonAi_v"+str(version)
        })
    return reports


def get_zip(bucket_name, source_blob_name, destination_file_name=None):
    #connect to google
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    if destination_file_name is None:
        os.makedirs("temp", exist_ok=True)
        destination_file_name = f"temp/training_data.zip"

    #if no directory exist for filepath create one
    if os.path.dirname(destination_file_name):
        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
    #download the zip file to destination file name
    blob.download_to_filename(destination_file_name)
    # Extract the contents of the zip file to a folder, eg destination - .zip
    extract_path = os.path.splitext(destination_file_name)[0]
    # Extract the contents
    with zipfile.ZipFile(destination_file_name, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    # Remove the zip file after extraction
    os.remove(destination_file_name)
    # Return the path to the extracted folder
    return extract_path