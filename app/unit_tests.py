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
            requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)
                

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
        

    # def test_graceful_shutdown(self):
    #     # Tests the graceful shutdown endpoint
    #     response = requests.get('http://127.0.0.1:5000/api/graceful_shutdown')
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
    #     self.assertIn('message', data)
    #     self.assertEqual(data['message'], 'Shutting down gracefully')
        
    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down unittests")


if __name__ == '__main__':
    unittest.main()
