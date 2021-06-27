"""
Package: app

Package for the application models and services
This module also sets up the logging to be used with gunicorn
"""
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config["LOGGING_LEVEL"] = logging.INFO

from service import routes, models, error_handlers

# Set up logging for production
print("Setting up logging for {}...".format(__name__))
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        app.logger.propagate = False
    else:
        routes.initialize_logging()
    routes.init_db()  # make our sqlalchemy tables

app.logger.info("Logging established")
