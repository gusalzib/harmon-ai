import tensorflow_model_analysis as tfma
from google.protobuf import text_format
import tensorflow as tf
import tensorflow_model_analysis.view as tfma_view
from ipywidgets.embed import embed_minimal_html
import io
import re

def generate_report(model_dir, tf_record_path):
    
   # eval config determines the format of the report 
    eval_config = text_format.Parse("""
      model_specs {
        signature_name: "serving_default"
        label_keys { key: "key" value: "key_label" }
        label_keys { key: "quality" value: "quality_label" }
      }
      
      # Slicing specs determine the rows of your report
      slicing_specs { } 
      slicing_specs { feature_keys: ["slice_key"] }
      slicing_specs { feature_keys: ["slice_quality"] }
      
      # --- METRICS FOR 'KEY' HEAD ---
      metrics_specs {
        output_names: ["key"]
        # High-level accuracy is enough for the summary table
        metrics { class_name: "SparseCategoricalAccuracy" }
        metrics { class_name: "ExampleCount" }
      }
      metrics_specs {
        output_names: ["key"]
        # The Plot handles the detailed breakdown visually
        metrics { class_name: "MultiClassConfusionMatrixPlot" }
      }

      # --- METRICS FOR 'QUALITY' HEAD ---
      metrics_specs {
        output_names: ["quality"]
        metrics { class_name: "SparseCategoricalAccuracy" }
        metrics { class_name: "ExampleCount" }
      }
      metrics_specs {
        output_names: ["quality"]
        metrics { class_name: "MultiClassConfusionMatrixPlot" }
      }
    """, tfma.EvalConfig())

    # Run the model analysis
    eval_result = tfma.run_model_analysis(
        eval_shared_model=tfma.default_eval_shared_model(
            eval_saved_model_path=model_dir,
            tags=[tf.saved_model.SERVING]
        ),
        data_location=tf_record_path,
        eval_config=eval_config,
        file_format='tfrecords'
    )

    # Render the results to an HTML string
    slicing_metrics_view = tfma_view.render_slicing_metrics(eval_result)

    views = [slicing_metrics_view]

    # eval_result.plots is a list of (slicing_spec, plots_dict) tuples.
    for slicing_spec, plots_dict in eval_result.plots:
        is_overall = False
        
        # 1. robust check for "Overall" slice
        if isinstance(slicing_spec, tuple):
            if len(slicing_spec) == 0:
                is_overall = True
        elif hasattr(slicing_spec, 'feature_values'):
            if not slicing_spec.feature_values:
                is_overall = True
        
        # 2. Render plots only for the overall slice
        if is_overall:
            for output_name in plots_dict.keys():
                views.append(
                    tfma_view.render_plot(
                        eval_result, 
                        slicing_spec=slicing_spec, 
                        output_name=output_name
                    )
                )

    html_file = io.StringIO()
    # Adding a title creates a cleaner header
    embed_minimal_html(html_file, views=views, title="Model Evaluation Summary")
    html_content = html_file.getvalue()
    html_file.close()

    # --- REGEX PATCHES ---
    # used Gen ai to troubleshoot html widget error 
    html_content = re.sub(
        r'html-manager@[\^]?[\d\.]+\/dist\/',
        'html-manager@0.20.0/dist/',
        html_content
    )

    # FIX THE 404
    tfma_js_url = f"https://unpkg.com/tensorflow_model_analysis@{tfma.__version__}/dist/tensorflow_model_analysis"
    
    html_content = html_content.replace(
        '"tensorflow_model_analysis": "tensorflow_model_analysis"', 
        f'"tensorflow_model_analysis": "{tfma_js_url}"'
    )
    html_content = html_content.replace(
        "tensorflow_model_analysis.js", 
        f"{tfma_js_url}.js"
    )

    print(f"Successfully generated clean evaluation report.")
    return html_content