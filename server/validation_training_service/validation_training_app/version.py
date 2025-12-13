from google.cloud import storage
import re

def version_model(bucket_name, model_name_prefix):
    """
    Checks a GCS bucket for models with a given prefix and determines the next version number.

    For example, if the bucket contains directories like:
    - 'models/HarmonAi_v1/'
    - 'models/HarmonAi_v2/'
    and you call version_model("your-bucket", "models/HarmonAi"),
    this function will return 3.

    Args:
        bucket_name (str): The name of the GCS bucket.
        model_name_prefix (str): The common prefix for the model directories, without the version
                                 (e.g., "models/HarmonAi").

    Returns:
        int: The next version number to use.
    """
    storage_client = storage.Client()
    # The prefix for listing blobs should include the start of the version part
    list_prefix = f"{model_name_prefix}_v"

    # We use a delimiter to treat the bucket like a filesystem and find "directories"
    iterator = storage_client.list_blobs(bucket_name, prefix=list_prefix, delimiter='/')

    # To get prefixes, we must iterate through the pages of the iterator.
    prefixes = set()
    for page in iterator.pages:
        prefixes.update(page.prefixes)

    if not prefixes:
        return 1

    max_version = 0
    # Regex to find the version number (e.g., the '2' in 'models/HarmonAi_v2/')
    version_regex = re.compile(r'_v(\d+)/?$')
    for prefix in prefixes:
        match = version_regex.search(prefix)
        if match:
            version = int(match.group(1))
            if version > max_version:
                max_version = version

    return max_version + 1

    
