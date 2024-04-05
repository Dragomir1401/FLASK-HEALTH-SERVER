"""Docstring: __init__ point of the application.
This is where the application is initialized and the Flask app is created."""

from flask import Flask
from app.data_ingestor import DataIngestor
from app.data_parser import DataParser
from app.task_runner import ThreadPool

WEB_SERVER = Flask(__name__)
WEB_SERVER.tasks_runner = ThreadPool()

# Read the csv path from nutrition_activity_obesity_usa_subset.csv
WEB_SERVER.data_ingestor = DataIngestor("nutrition_activity_obesity_usa_subset.csv")
WEB_SERVER.data_parser = DataParser(WEB_SERVER.data_ingestor)
WEB_SERVER.job_counter = 1
WEB_SERVER.is_shutdown = False

from app import routes
