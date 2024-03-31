import unittest
import requests
from app import webserver
from app.logger import logger

class TestServerEndpoints(unittest.TestCase):
    def setUp(self):
        # This method will run before each test method.
        webserver.job_counter = 1
        logger.info("Setting up unittests")



    def test_jobs(self):
        # Tests the jobs status endpoint
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'done')
        self.assertIsInstance(data['data'], list)

    def test_num_jobs(self):
        # Tests the number of jobs endpoint
        response = requests.get('http://127.0.0.1:5000/api/num_jobs')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('num_jobs', data)
        self.assertIsInstance(data['num_jobs'], int)

    def test_graceful_shutdown(self):
        # Tests the graceful shutdown endpoint
        response = requests.get('http://127.0.0.1:5000/api/graceful_shutdown')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Shutting down gracefully')
        
    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down unittests")


if __name__ == '__main__':
    unittest.main()
