"""This module sets up a logger for the web server."""
import logging
import time
from logging.handlers import RotatingFileHandler

def setup_logger(level=logging.INFO):
    """Set up a logger for the web server."""
    logger = logging.getLogger('WebServerLogger')
    logger.setLevel(level)

    # Create a rotating file handler
    handler = RotatingFileHandler('webserver.log', maxBytes=10240, backupCount=5)
    handler.setLevel(level)

    # Create a logging format with UTC timestamps
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')  # Adjusted indentation here
    formatter.converter = time.gmtime  # Use UTC time
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger

class Logger:
    """Class to set up a logger for the web server."""
    def __init__(self):
        self.logger = setup_logger()

    def info(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'INFO'."""
        self.logger.info(msg, *args, **kwargs)

    # Example of adding another method to address the linter's too-few-public-methods warning
    def error(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'ERROR'."""
        self.logger.error(msg, *args, **kwargs)
