import os
import logging
import logging.handlers

# Create a logger
logger = logging.getLogger('Chat_logger')
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

# Create a file handler
fh = logging.handlers.RotatingFileHandler(os.environ["LOG_FILE"], maxBytes=1000000, backupCount=5)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(ch)
logger.addHandler(fh)
