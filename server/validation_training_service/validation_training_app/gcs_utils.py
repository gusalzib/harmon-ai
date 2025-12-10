from google.cloud import storage

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