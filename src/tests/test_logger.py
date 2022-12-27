import unittest
import logging
import os
from src.my_logger import Logger
import re
from distutils.dir_util import remove_tree
import time

class TestLoggerCreation(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "testlog")

        if os.path.isdir(self.test_dir):
            remove_tree(self.test_dir)

    def test_instantiation(self):
        logger = Logger(self.test_dir, "myname")

        self.assertEqual(logger.name, "myname")
    
    def test_no_name_used_root_logger(self):

        logger = Logger(self.test_dir)

        self.assertEqual(logger.name, 'root')
    
    def test_log_directory_set(self):
        logger = Logger(self.test_dir)
        self.assertEqual(logger.log_base_directory, self.test_dir)

    def test_log_timestamp_correct_format(self):

        logger = Logger(self.test_dir)

        match = re.search(r"\d{4}-\d{2}-\d{2}--\d{2}-\d{2}-\d{2}", logger.init_time)
        self.assertFalse(match is None)
    
    def test_log_directories_created(self):
        logger = Logger(self.test_dir)

        self.assertTrue(os.path.isdir(self.test_dir))
        
        dir_content = next(os.walk(self.test_dir))
        self.assertEqual(len(dir_content[1]), 1, "There should be one directory in base directory.")
        self.assertEqual(len(dir_content[2]), 0, "There should be no files here.")

        match = re.search(r"\d{4}-\d{2}-\d{2}--\d{2}-\d{2}-\d{2}", dir_content[1][0])

        self.assertTrue(match is not None, "Subdir should be in datetime format.")

        subdir_content = next(os.walk(os.path.join(dir_content[0],dir_content[1][0])))

        self.assertEqual(len(subdir_content[1]), 0, "There should be no directories in subdir.")
        self.assertEqual(subdir_content[2][0], "log.txt", "There should be a log.txt file in subdir.")
        self.assertEqual(len(subdir_content[2]), 1, "There should only be one file created in subdir.")

    def test_active_loggers_added_to_list(self):

        logger1 = Logger(self.test_dir)

        self.assertListEqual(Logger._active_logs, [logger1.log_directory])

        time.sleep(1)
        logger2 = Logger(self.test_dir)
        time.sleep(2)
        logger3 = Logger(self.test_dir)

        self.assertListEqual(Logger._active_logs,
        [logger1.log_directory, logger2.log_directory, logger3.log_directory])

        del(logger2)

        self.assertListEqual(Logger._active_logs,
        [logger1.log_directory, logger3.log_directory])
        

    def test_logdir_init_doesnt_clean_tree_by_default(self):
        test_file = os.path.join(self.test_dir, 'myfile.txt')

        os.makedirs(self.test_dir)
        with open(test_file, "w") as f:
            f.write("hello")

        logger = Logger(self.test_dir)

        self.assertTrue(os.path.isfile(test_file))
    
    def tearDown(self):
        if os.path.isdir(self.test_dir):
            remove_tree(self.test_dir)

class TestLogRemoval(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "testlog")

        if os.path.isdir(self.test_dir):
            remove_tree(self.test_dir)
        
        new_folder = os.path.join(self.test_dir, "new_folder")
        new_file = os.path.join(new_folder, "log.txt")

        os.makedirs(new_folder)
        with open(new_file, "w") as f:
            pass

    def test_active_logs_not_cleaned(self):
        logger = Logger(self.test_dir)
        time.sleep(1)
        logger2 = Logger(self.test_dir)

        logger2.clean_logs()

        logs = next(os.walk(self.test_dir))[1]

        self.assertEqual(len(logs), 3)

    def test_empty_inactive_logs_cleaned(self):
        logger = Logger(self.test_dir)
        time.sleep(1)
        logger2 = Logger(self.test_dir)
        del(logger)
        logger2.clean_logs()

        logs = next(os.walk(self.test_dir))[1]

        self.assertEqual(len(logs), 2)
    
    def test_nonempty_inactive_logs_not_cleaned(self):
        logger = Logger(self.test_dir)
        logger.warning("A warning")
        time.sleep(1)
        logger2 = Logger(self.test_dir)
        del(logger)
        logger2.clean_logs()

        logs = next(os.walk(self.test_dir))[1]

        self.assertEqual(len(logs), 3)

    def tearDown(self):
        if os.path.isdir(self.test_dir):
            remove_tree(self.test_dir)


if __name__ == "__main__":
    unittest.main()