from my_logger import Logger
import os
class App:

    def __init__(self):
        """Initialises the searcher."""

        self.log_dir = os.path.join(os.path.dirname(__file__), "logs")
        self.logger = Logger(self.log_dir, __name__)
        self.logger.info("Log started")

def main():
    app = App()

    a=1
if __name__ == "__main__":
    main()

