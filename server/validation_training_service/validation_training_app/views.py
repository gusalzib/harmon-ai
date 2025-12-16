from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import json
from .data_preprocessing import load_data, create_test_train_validationset, save_testdata_to_tfrecord
from .training import build_model, train_model, save_serving_model, save_model_for_tfma
from .evaluation import generate_report
from .version import version_model, version_clean_data
from .gcs_utils import upload_blob_from_string, get_all_reports, get_zip, upload_blob_from_file
from .vetl_orchestrator import vetl_orchestrator


 # --- Configuration ---
BUCKET_NAME = "harmon_ai"
MODEL_NAME = "HarmonAi"
BASE_MODEL_PATH = "models" # GCS "folder"
BASE_REPORT_PATH = "reports" # GCS "folder"
BASE_CLEAN_DATA_PATH = "data/clean_data" # GCS "folder"






@csrf_exempt
def test_train_model(request):
    if request.method == 'POST':
        # Debugging: Print the raw body and headers to the console/logs
        print(f"DEBUG: Raw Request Body: {request.body!r}", flush=True)
        print(f"DEBUG: Content-Type: {request.content_type}", flush=True)

        dataset_name = None

        if 'dataset_name' in request.POST:
            dataset_name = request.POST['dataset_name']
        
        # 2. If not found, try parsing body as JSON or raw string
        if not dataset_name:
            try:
                body_str = request.body.decode('utf-8')
                if body_str:
                    try:
                        data = json.loads(body_str)
                        if isinstance(data, dict):
                            dataset_name = data.get('dataset_name')
                        else:
                            dataset_name = str(data)
                    except json.JSONDecodeError:
                        # Fallback: treat entire body as the name
                        dataset_name = body_str
            except Exception:
                pass
        
        # Ensure we have a string and clean it
        if dataset_name:
            dataset_name = dataset_name.strip().strip('"').strip("'")


        if not dataset_name:
            return JsonResponse({
                "status": "error", 
                "message": "No dataset name provided",
                "debug_received_body": request.body.decode('utf-8', errors='ignore')
            }, status=400)

        # The frontend uploads to 'data/' folder in GCS
        try:
            dataset_path = get_zip(BUCKET_NAME, f"data/{dataset_name}")
        except Exception as e:
            print(f"ERROR: Failed to download/extract zip: {e}", flush=True)
            return JsonResponse({"status": "error", "message": f"Failed to process dataset: {str(e)}"}, status=500)
        
        # Handle nested folder structures (e.g. if the user zipped a folder containing the data)
        # The orchestrator expects 'billboard-2.0-chordino' to be in the dataset_path
        required_subfolder = "billboard-2.0-chordino"
        if not os.path.exists(os.path.join(dataset_path, required_subfolder)):
            try:
                # Check if there is a single subdirectory containing the data
                subdirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
                if len(subdirs) == 1:
                    nested_path = os.path.join(dataset_path, subdirs[0])
                    if os.path.exists(os.path.join(nested_path, required_subfolder)):
                        print(f"DEBUG: Adjusting dataset path to nested folder: {subdirs[0]}", flush=True)
                        dataset_path = nested_path
            except Exception as e:
                print(f"WARNING: Error checking dataset structure: {e}", flush=True)
        
        # Version the training data output (training_data_vX)
        dataset_version = version_clean_data(BUCKET_NAME, f"{BASE_CLEAN_DATA_PATH}/training_data")

        orchestrator_results = vetl_orchestrator(dataset_version, dataset_path)
        if not orchestrator_results:
            return JsonResponse({"status": "error", "message": "Pipeline failed during validation or merging."}, status=500)
            
        db_path = orchestrator_results['db_path']
        
        # Upload with versioned name to GCS
        upload_blob_from_file(BUCKET_NAME, db_path, f"{BASE_CLEAN_DATA_PATH}/training_data_v{dataset_version}.db")

        # 1. Get the next model version
        next_version = version_model(BUCKET_NAME, f"{BASE_MODEL_PATH}/{MODEL_NAME}")
        versioned_model_name = f"{MODEL_NAME}_v{next_version}"
        
        # Define GCS destination paths
        gcs_serving_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/serving"
        gcs_tfma_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/tfma"
        gcs_tfrecord_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/test_data.tfrecord"
        gcs_report_path = f"{BASE_MODEL_PATH}/{BASE_REPORT_PATH}/{versioned_model_name}_report.html"

        # 2. Load and preprocess data 
        ##change load data to use sql path as parameter
        dataset = load_data(db_path)
        train_dataset, val_dataset, test_dataset = create_test_train_validationset(dataset)

        # 3. Train the model
        model = build_model()
        train_model(model, train_dataset, val_dataset)

        # 4. Save model artifacts and test data directly to Google cloud storage
        print("Saving models and test data directly to GCS...")
        save_serving_model(model, gcs_serving_path)
        save_model_for_tfma(model, gcs_tfma_path)
        save_testdata_to_tfrecord(gcs_tfrecord_path, test_dataset)

        # 5. Evaluate model and generate report
        print("Generating TFMA evaluation report...")
        report_content = generate_report(gcs_tfma_path, gcs_tfrecord_path)

        # 6. Upload the HTML report from memory to GCS
        print("Uploading evaluation report to GCS...")
        upload_blob_from_string(BUCKET_NAME, report_content, gcs_report_path)

        return JsonResponse({"status": "success", "message": f"Model training for {versioned_model_name} complete."})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@csrf_exempt
def fetch_reports(request):
    if request.method == 'GET':
        # path of reports
        path = BASE_MODEL_PATH +"/"+ BASE_REPORT_PATH
        # get all reports
        reports = get_all_reports(BUCKET_NAME,path)
        # return reports
        return JsonResponse({"reports":reports})

        