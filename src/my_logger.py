import logging
import os
import re
from datetime import datetime
from distutils.dir_util import remove_tree

class Logger(logging.Logger):
    _active_logs = []

    def __init__(self,log_directory: str, name: str="root", *,
    clean_logs: bool=True):
        """Initialises the class and creates the logger with requested name.
        
        Args:
            log_directory: Base directory of Logger.
            name: Name of the logger.
            clean_logs: Cleans empty Log files if true.
        Returns:
            None.
        """
        if not isinstance(log_directory, str):
            log_directory = str(log_directory)

        super().__init__(name)

        self.log_base_directory = log_directory

        self.init_time = self.get_creation_time()
        self.log_directory = os.path.join(self.log_base_directory, self.init_time)
        self.log_file = os.path.join(self.log_directory, "log.txt")

        __class__._active_logs.append(self.log_directory)

        self.init_log_directory()
        self.init_logger()

        if clean_logs:
            self.clean_logs()
    
    def __del__(self):
        __class__._active_logs.remove(self.log_directory)

    def init_logger(self):
        """Initialises the output streams of the loggger."""
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(self.log_file, mode="w")

        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.WARNING)

        c_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        f_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )

        self.addHandler(c_handler)
        self.addHandler(f_handler)

        self.setLevel(logging.DEBUG)

    @staticmethod
    def get_creation_time():
        """Gets a timestamp of the current time."""

        return datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    
    def clean_logs(self):
        """Iterates through log directories and removes empty logs."""
        try:
            content = next(os.walk(self.log_base_directory))
        except StopIteration:
            return

        dirs = [x for x in content[1] if
            re.search(r"\d{4}-\d{2}-\d{2}--\d{2}-\d{2}-\d{2}", x) is not None and
            os.path.join(self.log_base_directory, x) not in Logger._active_logs]

        for log_folder in dirs:
            log_folder_path = os.path.join(self.log_base_directory, log_folder)
            log_file = os.path.join(log_folder_path, "log.txt")
            
            if not os.path.isfile(log_file) or os.path.getsize(log_file) == 0:
                remove_tree(log_folder_path)

    def init_log_directory(self):
        """Creates the log directory if it does not already exist. Removes directory first if `clean` set to True."""

        if not os.path.isdir(self.log_directory):
            os.makedirs(self.log_directory)
        