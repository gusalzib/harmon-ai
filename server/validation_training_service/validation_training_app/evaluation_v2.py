import tensorflow as tf
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score
import json


# Key map as per the LabelEncoder output 
all_possible_keys = {
    0: "A",
    1: "A#",
    2: "B", 
    3: "C",
    4: "C#",
    5: "D",
    6: "D#",
    7: "E",
    8: "F",
    9: "F#",
    10: "G",
    11: "G#",
    12: "N",
    13: "X"
}

# Quality nap as per the LabelEncoder output
all_possible_qualities = {
    0: "7", 
    1: "None", 
    2: "maj", 
    3: "min"
}

def calculate_metrics(true_labels, pred_labels, annotation_ids):
    annotation_slices = set(annotation_ids)
    metrics_per_slice = {}

    true_labels = np.array(true_labels)
    pred_labels = np.array(pred_labels)

    for annotation in annotation_slices:
        annotation_indices = [i for i, s in enumerate(annotation_ids) if s == annotation]

        if annotation_indices: # do we have any?
            annotation_ground_truth = true_labels[annotation_indices]
            annotation_prediction = pred_labels[annotation_indices]
            annotation_accuracy = accuracy_score(annotation_ground_truth, annotation_prediction)
            metrics_per_slice[annotation] = {
                "accuracy": float(annotation_accuracy),
                "number_of_examples": int(len(annotation_ground_truth))
                }
    return metrics_per_slice


def evaluate_model(model, test_dataset):
    all_key_preds = []
    all_key_labels = []
    all_quality_preds = []
    all_quality_labels = []

    # storing which "annotation" each record belongs to
    # analysis per category basically 
    all_grouped_by_keys = []
    all_grouped_by_qualities = []

    print("starting analyses. . . \n")

    for x, y in test_dataset: 
        predictions = model(x, training=False)
        key_pred = predictions['key']
        quality_pred = predictions['quality']

        key_pred_numerical = tf.argmax(key_pred, axis=1).numpy()
        quality_pred_numerical = tf.argmax(quality_pred, axis=1).numpy()

        key_ground_truth = y['key'].numpy()
        quality_ground_truth = y['quality'].numpy()

        all_key_preds.extend(key_pred_numerical)
        all_key_labels.extend(key_ground_truth)
        all_quality_preds.extend(quality_pred_numerical)
        all_quality_labels.extend(quality_ground_truth)

        all_grouped_by_keys.extend([all_possible_keys.get(int(k), str(k)) for k in key_ground_truth])
        all_grouped_by_qualities.extend([all_possible_qualities.get(int(q), str(q)) for q in quality_ground_truth])

    # converting to numpy arrays
    all_key_preds = np.array(all_key_preds)
    all_key_labels = np.array(all_key_labels)
    all_quality_preds = np.array(all_quality_preds)
    all_quality_labels = np.array(all_quality_labels)

    # calculating metrics
    key_accuracy = accuracy_score(all_key_labels, all_key_preds)
    quality_accuracy = accuracy_score(all_quality_labels, all_quality_preds)
    total_examples = len(all_key_labels)

    # confusion metrics
    key_confusion_matrix = confusion_matrix(all_key_labels, all_key_preds).tolist()
    quality_confusion_matrix = confusion_matrix(all_quality_labels, all_quality_preds).tolist()


    key_class_labels = []
    for class_index in range(len(key_confusion_matrix)):
        
        chord_name = all_possible_keys.get(class_index, str(class_index))
        key_class_labels.append(chord_name)

    
    quality_class_labels = []
    for class_index in range(len(quality_confusion_matrix)):
    
        quality_name = all_possible_qualities.get(class_index, str(class_index))
        quality_class_labels.append(quality_name)


    # per annotation 
    key_slice_metrics = calculate_metrics(
        all_key_labels,
        all_key_preds,
        all_grouped_by_keys
    )

    quality_slice_metrics = calculate_metrics(
        all_quality_labels,
        all_quality_preds,
        all_grouped_by_qualities
    )

    results = {
        "overall_metrics": {
            "total_examples": int(total_examples),
            "key": {
                "accuracy": float(key_accuracy),
                "confusion_matrix": key_confusion_matrix,
                "class_labels": key_class_labels
            }, 
            "quality": {
                "accuracy": float(quality_accuracy),
                "confusion_matrix": quality_confusion_matrix,
                "class_labels": quality_class_labels
            }
        },
        "annotations": {
            "key_annotations": key_slice_metrics,
            "quality_annotations": quality_slice_metrics
        }
    }

    print("End of evaluation. . . \n")
    return results



def generate_report(model, test_dataset):
    print("starting evaluation of model . . .")

    metrics = evaluate_model(model, test_dataset)

    json_report = json.dumps(metrics)

    return json_report

