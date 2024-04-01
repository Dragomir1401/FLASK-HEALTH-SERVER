import unittest
import requests
from app import webserver
from app.logger import logger
import json
import os

class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        # This method will run before each test method.
        webserver.job_counter = 1
        logger.info("Setting up unittests")
    
    def helper_test_endpoint(self, endpoint, file_name):
        input_file = f"./my_unittests/{endpoint}/input/{file_name}"

        # Get the index from in-idx.json
        # The idx is between a dash (-) and a dot (.)
        idx = input_file.split('-')[1]
        idx = int(idx.split('.')[0])

        with open(f"{input_file}", "r") as fin:
            # Data to be sent in the POST request
            req_data = json.load(fin)

        with self.subTest():
            # Sending a POST request to the Flask endpoint
            res = requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)
            job_id = res.json()
            job_id = job_id["job_id"]
            result = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")

            return result

    def test_state_mean(self):
        # Read ref results from out-idx.json
        with open("./my_unittests/state_mean/output/out-1.json", "r") as fout:
            ref_result = json.load(fout)

        key_ref, val_ref = ref_result.keys(), ref_result.values()

        # Tests the state_mean endpoint
        result = self.helper_test_endpoint("state_mean", "in-1.json")
        self.assertEqual(result.status_code, 200)

        data = result.json()
        data = data["data"]

        # Extract key-value pair
        key, val = data.keys(), data.values()

        self.assertEqual(key, key_ref)
        print (val)

        # Extract the value from the dictionary dict_values([value])
        val = list(val)[0]
        val_ref = list(val_ref)[0]

        self.assertAlmostEqual(val, val_ref, delta=0.0001)

        # Log the unit test results
        logger.info("Unit test state_mean passed")

    def test_jobs(self):
        # Do a jobs request to create see what jobs are now available
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        # Get old job ids from data field in json response
        data = response.json()
        old_job_ids = data['data']

        # Do 3 state_mean requests to create 3 job ids
        self.helper_test_endpoint("state_mean", "in-1.json")
        self.helper_test_endpoint("state_mean", "in-2.json")
        self.helper_test_endpoint("state_mean", "in-1.json")

        # Tests the jobs status endpoint
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'done')
        self.assertEqual(len(data['data']), len(old_job_ids) + 3)

        # Assert that the last 3 entries from the new job ids are not in the old job ids
        self.assertNotIn(data['data'][-1], old_job_ids)
        self.assertNotIn(data['data'][-2], old_job_ids)
        self.assertNotIn(data['data'][-3], old_job_ids)

        # Log the unit test results
        logger.info("Unit test jobs passed")
        # Log the 3 new job ids
        logger.info("New job ids:")
        logger.info(data['data'][-1])
        logger.info(data['data'][-2])
        logger.info(data['data'][-3])

    def test_num_jobs(self):
        # Tests the number of jobs endpoint
        # Do a num_jobs request to create see what jobs are now available
        response = requests.get('http://127.0.0.1:5000/api/num_jobs')
        # Get old job ids from data field in json response
        data = response.json()
        old_num_jobs = data['num_jobs']

        # Do 3 state_mean requests to create 3 job ids
        self.helper_test_endpoint("state_mean", "in-1.json")
        self.helper_test_endpoint("state_mean", "in-2.json")
        self.helper_test_endpoint("state_mean", "in-1.json")

        # Tests the num_jobs status endpoint
        response = requests.get('http://127.0.0.1:5000/api/num_jobs')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data['num_jobs'], old_num_jobs + 3)

        # Log the unit test results
        logger.info("Unit test jobs passed")
        # Log the old number of jobs
        logger.info("Old number of jobs:")
        logger.info(old_num_jobs)
        # Log the number of new jobs
        logger.info("New number of jobs:")
        logger.info(data['num_jobs'])

    def test_zzz_graceful_shutdown(self):
        # Test that the server sends 503 Unavailable after shutdown
        # Send a shutdown request
        response = requests.get('http://127.0.0.1:5000/api/graceful_shutdown')
        self.assertEqual(response.status_code, 200)

        logger.info("Shutting down server")

        # Send a state_mean request
        response = requests.post('http://127.0.0.1:5000/api/state_mean', json={"state": "CA"})
        self.assertEqual(response.status_code, 503)

        # Log the unit test results
        logger.info("Unit test graceful_shutdown passed")

        
    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down unittests")


if __name__ == '__main__':
    unittest.main()
