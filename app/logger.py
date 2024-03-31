import logging
from logging.handlers import RotatingFileHandler
import time

def setup_logger():
    logger = logging.getLogger('WebServerLogger')
    logger.setLevel(logging.INFO)

    # Create a rotating file handler
    handler = RotatingFileHandler('webserver.log', maxBytes=10240, backupCount=5)
    handler.setLevel(logging.INFO)

    # Create a logging format with UTC timestamps
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    formatter.converter = time.gmtime  # Use UTC time
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

# Initialize logger
logger = setup_logger()
