from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from .data_preprocessing import load_data, create_test_train_validationset, save_testdata_to_tfrecord
from .training import build_model, train_model, save_serving_model, save_model_for_tfma
from .evaluation import generate_report
from .version import version_model
from .gcs_utils import upload_blob_from_string, get_all_reports, get_zip


 # --- Configuration ---
BUCKET_NAME = "harmon_ai"
MODEL_NAME = "HarmonAi"
BASE_MODEL_PATH = "models" # GCS "folder"
BASE_REPORT_PATH = "reports" # GCS "folder"




@csrf_exempt
def test_train_model(request):
    if request.method == 'POST':
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
        dataset = load_data()
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
        path = BASE_MODEL_PATH +"/"+ BASE_REPORT_PATH
        reports = get_all_reports(BUCKET_NAME,path)
        print(reports)

        return JsonResponse({"reports":reports})

        