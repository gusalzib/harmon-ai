import tensorflow_model_analysis as tfma
from google.protobuf import text_format
import tensorflow as tf
import data_preprocessing as dp
from tensorflow_model_analysis.notebook.jupyter.renderer import render_slicing_metrics_to_html


def generate_report(model_dir, tf_record_path):
    
    # Define the TFMA evaluation configuration
    eval_config = text_format.Parse("""
      model_specs {
        signature_name: "serving_default"
        label_key: { key: "key" value: "key_label" }
        label_key: { key: "quality" value: "quality_label" }
      }
      slicing_specs { } 
      slicing_specs { feature_keys: ["slice_key"] }
      slicing_specs { feature_keys: ["slice_quality"] }
      
      metrics_specs {
        output_name: "key"
        metrics { class_name: "SparseCategoricalAccuracy" }
        metrics { class_name: "ExampleCount" }
      }
      metrics_specs {
        output_name: "quality"
        metrics { class_name: "SparseCategoricalAccuracy" }
        metrics { class_name: "ExampleCount" }
      }
    """, tfma.EvalConfig())

    eval_result = tfma.run_model_analysis(
        eval_shared_model=tfma.default_eval_shared_model(
            eval_saved_model_path=model_dir,
            tags=[tf.saved_model.SERVING]
        ),
        data_location=tf_record_path,
        eval_config=eval_config,
        file_format='tfrecords'
    )

    # Render the results to an HTML file
    html_content = render_slicing_metrics_to_html(eval_result)
    print(f"Successfully generated evaluation report content.")
    return html_content
