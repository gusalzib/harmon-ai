from google.cloud import storage
import re

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


def get_all_reports(bucket_name,path_to_reports):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    reports = []
    for blob in bucket.list_blobs(prefix=path_to_reports):
        if blob.name.endswith('/'):
            continue
        match = re.search(r'_v(\d+)', blob.name)
        version = int(match.group(1)) if match else None
        if version is None:
            print(f"Warning: No version found in {blob.name}")
        reports.append({
            "url": blob.public_url,
            "version": version,
            "name": "HarmonAi_v"+str(version)
        })
    return reports