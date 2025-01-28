import logging

class Log:

    def __init__(self):
        self.logger = self._setup_logger()
    
    @staticmethod
    def _setup_logger():
        # Create a logger object
        logger = logging.getLogger("stdout_logger")
        logger.setLevel(logging.DEBUG)  # Set logging level

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set level for handler

        # Define a formatter with a date-time prefix
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Attach the formatter to the handler
        console_handler.setFormatter(formatter)

        # Attach the handler to the logger
        logger.addHandler(console_handler)

        return logger
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)