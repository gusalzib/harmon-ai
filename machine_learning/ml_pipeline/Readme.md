1. I have to add ml-pipeline to the validation_training_app
2. In views: you receive a request in     if request.method == 'POST':
3. unzip the folder received from Ibrahim/frontend in this request, using the unzip method that Viktor wrote: 
3. then  ---> start the orchestrator go through the pipe 
4. check the versioning: in (version_clean_data in version.py) 
5. return sqlite to GCS (upload_blob_from_file in gcs_utils.py) 

pay attention to order between versioning and sqlite to GCS etc.


remember in sqlite saving: can do: sqlite_path = 'cleaned_data.db' # "cleaned_data_v{version}.db"
for versioning. Add versioning as a parameter to 