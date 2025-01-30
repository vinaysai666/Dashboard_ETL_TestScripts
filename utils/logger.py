import sys

sys.dont_write_bytecode = True

import logging

# Configure logging
logging.basicConfig(filename="validation.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_results(message):
    """Log validation results."""
    logging.info(message)
    print(message)