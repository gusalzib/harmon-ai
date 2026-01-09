from django.test import SimpleTestCase
from .vetl_orchestrator import vetl_orchestrator
import os

# Create your tests here.
class PipelineTestCase(SimpleTestCase):
    def test_valid_data(self):
        data_test_folder = "McGill-valid"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        self.assertNotEqual(result, None)

    # Only contains a single sample, 0006
    def test_single_set(self):
        data_test_folder = "McGill-single"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        self.assertNotEqual(result, None)

    # It's just a text file
    def test_literal_trash(self):
        data_test_folder = "McGill-trash"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions
        self.assertEqual(result, None)

    # 0006 majmin7.lab missing chords column
    def test_missing_columns(self):
        data_test_folder = "McGill-missing-columns"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions
        self.assertEqual(result, None)

    # Test if chronological timestamps may decrease. Moved chunk of bothchroma to misalign timestamp
    def test_non_sequential_timestamps(self):
        data_test_folder = "McGill-non-sequential"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions
        self.assertEqual(result, None)

    # C chord replaced with Q, maj replaced with mij, and min replaced with mao
    def test_invalid_values(self):
        data_test_folder = "McGill-invalid-values"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions
        self.assertEqual(result, None)

    # Chordino contains 0006 & 0010, mirex contains 0004 & 0006
    def test_dataset_mismatch(self):
        data_test_folder = "McGill-set-mismatch"
        dataset_version = 1
        test_data_path = os.path.join("validation_training_app", "testing_data", data_test_folder)
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions
        self.assertEqual(result, None)
