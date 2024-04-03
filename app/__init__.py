from flask import Flask
from app.data_ingestor import DataIngestor
from app.data_parser import DataParser
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
# FOR UNIT TESTS
# Change the csv_relative_path to unit_tests_csv_relative_path
filename = "unit_tests_csv_relative_path"

# Read from csv_relative_path file the path to the csv file
with open(filename, "r") as fin:
    csv_relative_path = fin.readline().strip()
    webserver.data_ingestor = DataIngestor(csv_relative_path)
    webserver.data_parser = DataParser(webserver.data_ingestor)
    webserver.job_counter = 1
    webserver.is_shutdown = False

from app import routes
