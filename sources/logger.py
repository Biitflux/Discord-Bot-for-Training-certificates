import os
import logging
import time
from logging import INFO, WARNING, ERROR

class CustomLogger:
    def __init__(self, log_folder="logs", log_level=logging.INFO):
        self.log_folder = log_folder
        os.makedirs(self.log_folder, exist_ok=True)
        
        log_filename = f"Bot-Log.{time.strftime('%Y-%m-%d_%H-%M-%S')}.log"
        log_filepath = os.path.join(self.log_folder, log_filename)

        formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    def log(self, message, level=logging.INFO):
        logging.log(level, message)
