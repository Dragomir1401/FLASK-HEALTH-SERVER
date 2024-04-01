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
    
    def helper_test_endpoint(self, endpoint):
        output_dir = f"./my_unittests/{endpoint}/output"
        input_dir = f"./my_unittests/{endpoint}/input"
        input_files = os.listdir(input_dir)

        for input_file in input_files:
            # Get the index from in-idx.json
            # The idx is between a dash (-) and a dot (.)
            idx = input_file.split('-')[1]
            idx = int(idx.split('.')[0])

            with open(f"{input_dir}/{input_file}", "r") as fin:
                # Data to be sent in the POST request
                req_data = json.load(fin)

            with open(f"{output_dir}/out-{idx}.json", "r") as fout:
                ref_result = json.load(fout)

            with self.subTest():
                # Sending a POST request to the Flask endpoint
                res = requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)

                job_id = res.json()
                # print(f'job-res is {job_id}')
                job_id = job_id["job_id"]

                result = requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}")
                self.assertEqual(result.status_code, 200)
                self.assertEqual(result, ref_result)
                

    def test_jobs(self):
        # Do 3 state_mean requests to create 3 job ids
        self.helper_test_endpoint("state_mean")
        self.helper_test_endpoint("state_mean")
        self.helper_test_endpoint("state_mean")

        # Tests the jobs status endpoint
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        print (response.status_code)
        print (response.json())
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'done')
        self.assertEqual(len(data['jobs']), 3)

    # def test_num_jobs(self):
    #     # Tests the number of jobs endpoint
    #     response = requests.get('http://127.0.0.1:5000/api/num_jobs')
    #     self.assertEqual(response.status_code, 200)
    #     data = response.json()
    #     self.assertIn('num_jobs', data)
    #     self.assertIsInstance(data['num_jobs'], int)

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
