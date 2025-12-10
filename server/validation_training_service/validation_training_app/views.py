from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import data_preprocessing as dp
import training as train
import evaluation as eval
from version import version_model
import gcs_utils


@csrf_exempt
def train_model(request):
    if request.method == 'POST':
        # --- Configuration ---
        BUCKET_NAME = "harmon_ai"
        MODEL_NAME = "HarmonAi"
        BASE_MODEL_PATH = "models" # GCS "folder"

        # 1. Get the next model version
        next_version = version_model(BUCKET_NAME, f"{BASE_MODEL_PATH}/{MODEL_NAME}")
        versioned_model_name = f"{MODEL_NAME}_v{next_version}"
        
        # Define GCS destination paths
        gcs_serving_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/serving"
        gcs_tfma_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/tfma"
        gcs_tfrecord_path = f"gs://{BUCKET_NAME}/{BASE_MODEL_PATH}/{versioned_model_name}/test_data.tfrecord"
        gcs_report_path = f"{BASE_MODEL_PATH}/{versioned_model_name}/evaluation_report.html"

        # 2. Load and preprocess data
        dataset = dp.load_data()
        train_dataset, val_dataset, test_dataset = dp.create_test_train_validationset(dataset)

        # 3. Train the model
        model = train.build_model()
        train.train_model(model, train_dataset, val_dataset)

        # 4. Save model artifacts and test data directly to GCS
        print("Saving models and test data directly to GCS...")
        train.save_serving_model(model, gcs_serving_path)
        train.save_model_for_tfma(model, gcs_tfma_path)
        dp.save_testdata_to_tfrecord(gcs_tfrecord_path, test_dataset)

        # 5. Evaluate model and generate report
        print("Generating TFMA evaluation report...")
        report_content = eval.generate_report(gcs_tfma_path, gcs_tfrecord_path)

        # 6. Upload the HTML report from memory to GCS
        print("Uploading evaluation report to GCS...")
        gcs_utils.upload_blob_from_string(BUCKET_NAME, report_content, gcs_report_path)

        return JsonResponse({"status": "success", "message": f"Model training for {versioned_model_name} complete."})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)