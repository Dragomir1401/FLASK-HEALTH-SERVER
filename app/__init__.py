from flask import Flask
from app.data_ingestor import DataIngestor
from app.data_parser import DataParser
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.data_parser = DataParser(webserver.data_ingestor)
webserver.job_counter = 1

from app import routes
