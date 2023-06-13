import logging
from datetime import datetime
from config import BASE_DIR
import os


def setup_logger():
    log_dir = str(BASE_DIR) + "/.log/"
    os.makedirs(log_dir, exist_ok=True)  # Create the log directory if it doesn't exist

    log_file = log_dir + datetime.now().strftime('%d-%m-%Y') + ".log"
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            pass  # Create an empty log file if it doesn't exist

    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name=None):
    return logging.getLogger(name)


# logger = get_logger()

