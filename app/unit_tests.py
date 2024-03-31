import unittest
import requests

class TestWebServerRoutes(unittest.TestCase):

    def test_graceful_shutdown(self):
        """Tests the graceful shutdown endpoint."""
        response = requests.get('http://127.0.0.1:5000/api/graceful_shutdown')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['message'], "Shutting down gracefully")

    def test_jobs(self):
        """Tests the jobs status endpoint."""
        response = requests.get('http://127.0.0.1:5000/api/jobs')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], "done")
        self.assertIsInstance(response_data['data'], list)

    def test_num_jobs(self):
        """Tests the number of jobs endpoint."""
        response = requests.get('http://127.0.0.1:5000/api/num_jobs')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('num_jobs', response_data)
        self.assertIsInstance(response_data['num_jobs'], int)

if __name__ == '__main__':
    unittest.main()
