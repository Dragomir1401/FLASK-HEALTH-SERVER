"""This module sets up a logger for the web server. """
import logging
import time
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self):
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Set up a logger for the web server."""
        logger = logging.getLogger('WebServerLogger')
        logger.setLevel(logging.INFO)

        # Create a rotating file handler
        handler = RotatingFileHandler('webserver.log', maxBytes=10240, backupCount=5)
        handler.setLevel(logging.INFO)

        # Create a logging format with UTC timestamps
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        formatter.converter = time.gmtime  # Use UTC time
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        return logger
    
    def info(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'INFO'."""
        self.logger.info(msg, *args, **kwargs)
