from django.test import TestCase
from . import vetl_orchestrator
import os

# Create your tests here.
class PipelineTestCase(TestCase):
    def test_valid_data(self):
        dataset_version = 1
        test_data_path = os.path.join("testing_data", "McGill-valid")
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        self.assertNotEqual(result, None)

    # It's just a text file
    def test_literal_trash(self):
        dataset_version = 1
        test_data_path = os.path.join("testing_data", "...")
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions

    # 
    def test_missing_columns(self):
        dataset_version = 1
        test_data_path = os.path.join("testing_data", "...")
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions

    # Test if chronological timestamps may decrease
    def test_non_sequential_timestamps(self):
        dataset_version = 1
        test_data_path = os.path.join("testing_data", "...")
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions

    # Test for e.g. Q chords and mij quality
    def test_unexpected_values(self):
        dataset_version = 1
        test_data_path = os.path.join("testing_data", "...")
        val_threshold = 1

        result = vetl_orchestrator(dataset_version, test_data_path, val_threshold)
        # Some assertions

