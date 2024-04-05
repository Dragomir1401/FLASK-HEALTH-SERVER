"""This file contains the unit tests for the server endpoints."""
import unittest
from time import sleep
import json
from app.data_ingestor import DataIngestor
from app.data_parser import DataParser

class TestServerEndpoints(unittest.TestCase):
    """Class to test the server endpoints."""
    def setUp(self):
        """Set up the test environment."""
        sleep(1)

    def test_global_mean(self):
        """Test the global_mean function."""
        data_ingestor = DataIngestor("./unittests/global_mean/global_mean.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/global_mean/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/global_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the global_mean function with the query
        result = data_parser.global_mean(query)

        result_scalar = result['Data_Value'].item()
        result_ref = ref_result['global_mean']

        # Now you can compare the scalar values
        self.assertAlmostEqual(result_scalar, result_ref, delta=0.0001,
                               msg="Data_Value does not match within the expected range")

        print("Test global_mean passed successfully.")

    def test_diff_from_mean(self):
        """Test the diff_from_mean function."""
        data_ingestor = DataIngestor("./unittests/diff_from_mean/diff_from_mean.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/diff_from_mean/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/diff_from_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the diff_from_mean function with the query
        result = data_parser.diff_from_mean(query)

        # Transform the result into a dictionary
        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))

        # Assert that the keys (LocationDesc) match
        self.assertEqual(data_dict.keys(), ref_result.keys(), "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small
        # delta for floating point comparison
        for key in data_dict.keys():
            self.assertAlmostEqual(data_dict[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test diff_from_mean passed successfully.")

    def test_state_diff_from_mean(self):
        """Test the state_diff_from_mean function."""
        data_ingestor = DataIngestor("./unittests/state_diff_from_mean/state_diff_from_mean.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/state_diff_from_mean/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/state_diff_from_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the state_diff_from_mean function with the query
        result = data_parser.state_diff_from_mean(query)

        # Since JSON keys are always strings, ensure the ref keys/values
        # are extracted correctly
        key_ref = list(ref_result.keys())[0]
        val_ref = list(ref_result.values())[0]

        # Execute the state_mean function with the query
        result = data_parser.state_mean(query)

        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))
        key = list(data_dict.keys())[0]
        val = list(data_dict.values())[0]

        # Assert that the keys (LocationDesc) match
        self.assertEqual(key, key_ref, "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small
        # delta for floating point comparison
        self.assertAlmostEqual(val, val_ref, delta=0.0001,
                               msg="Data_Value does not match within the expected range")

        print("Test state_diff_from_mean passed successfully.")

    def test_mean_by_category(self):
        """Test the mean_by_category function."""
        data_ingestor = DataIngestor("./unittests/mean_by_category/mean_by_category.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/mean_by_category/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/mean_by_category/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the mean_by_category function with the query
        result = data_parser.mean_by_category(query)

        # Compare each key as state with category to be equal
        self.assertEqual(result.keys(), ref_result.keys(),
                         "State or stratification does not match")

        # Compare each value with a tolerance of 0.0001
        for key in result:
            self.assertAlmostEqual(result[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test mean_by_category passed successfully.")

    def test_state_mean_by_category(self):
        """Test the state_mean_by_category function."""
        data_ingest = DataIngestor("./unittests/state_mean_by_category/state_mean_by_category.csv")
        data_parser = DataParser(data_ingest)

        # Read input query from in-idx.json
        with open("./unittests/state_mean_by_category/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/state_mean_by_category/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the state_mean_by_category function with the query
        result = data_parser.state_mean_by_category(query)

        # Compare each key as state with category to be equal
        self.assertEqual(result.keys(), ref_result.keys(), "State or stratification does not match")

        # Compare each value with a tolerance of 0.0001
        for key in result:
            self.assertAlmostEqual(result[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test state_mean_by_category passed successfully.")


    def test_state_mean(self):
        """Test the state_mean function."""
        data_ingestor = DataIngestor("./unittests/state_mean/state_mean.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/state_mean/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/state_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Since JSON keys are always strings, ensure the ref keys/values are extracted correctly
        key_ref = list(ref_result.keys())[0]
        val_ref = list(ref_result.values())[0]

        # Execute the state_mean function with the query
        result = data_parser.state_mean(query)

        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))
        key = list(data_dict.keys())[0]
        val = list(data_dict.values())[0]

        # Assert that the keys (LocationDesc) match
        self.assertEqual(key, key_ref, "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small delta for
        # floating point comparison
        self.assertAlmostEqual(val, val_ref, delta=0.0001,
                               msg="Data_Value does not match within the expected range")

        print("Test state_mean passed successfully.")

    def test_states_mean(self):
        """Test the states_mean function."""
        data_ingestor = DataIngestor("./unittests/states_mean/states_mean.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/states_mean/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/states_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the states_mean function with the query
        result = data_parser.states_mean(query)

        # Transform the result into a dictionary
        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))

        # Assert that the keys (LocationDesc) match
        self.assertEqual(data_dict.keys(), ref_result.keys(), "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small delta for
        # floating point comparison
        for key in data_dict.keys():
            self.assertAlmostEqual(data_dict[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test states_mean passed successfully.")

    def test_best5(self):
        """Test the best5 function."""
        data_ingestor = DataIngestor("./unittests/best5/best5.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/best5/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/best5/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the best5 function with the query
        result = data_parser.best5(query)

        # Transform the result into a dictionary
        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))

        # Assert that the keys (LocationDesc) match
        self.assertEqual(data_dict.keys(), ref_result.keys(), "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small delta for
        # floating point comparison
        for key in data_dict.keys():
            self.assertAlmostEqual(data_dict[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test best5 passed successfully.")

    def test_worst5(self):
        """Test the worst5 function."""
        data_ingestor = DataIngestor("./unittests/worst5/worst5.csv")
        data_parser = DataParser(data_ingestor)

        # Read input query from in-idx.json
        with open("./unittests/worst5/input/in-1.json", "r") as fin:
            query = json.load(fin)

        # Read ref results from out-idx.json
        with open("./unittests/worst5/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        # Execute the worst5 function with the query
        result = data_parser.worst5(query)

        # Transform the result into a dictionary
        data_dict = dict(zip(result['LocationDesc'], result['Data_Value']))

        # Assert that the keys (LocationDesc) match
        self.assertEqual(data_dict.keys(), ref_result.keys(), "LocationDesc does not match")

        # Assert that the values (Data_Value) are almost equal, with a small delta for
        # floating point comparison
        for key in data_dict.keys():
            self.assertAlmostEqual(data_dict[key], ref_result[key], delta=0.0001,
                                   msg="Data_Value does not match within the expected range")

        print("Test worst5 passed successfully.")

def main():
    """Run the unit tests."""
    unittest.main()
