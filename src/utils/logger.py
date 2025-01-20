import logging


class AppLogger:
    """
    A simple logger class that can be used to log messages with a specific format.
    
    Example usage:
    logger = AppLogger(__name__)
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    """

    def __init__(self, name: str = None) -> None:
        """
        Initializes the logger with the default logging format and level.
        """
        self.logger = logging.getLogger(name if name else __name__)
        logging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s",
            level=logging.INFO,
        )

    def info(self, message: str) -> None:
        """Logs an info message"""
        self.logger.info(message)

    def error(self, message: str) -> None:
        """Logs an error message"""
        self.logger.error(message)

    def debug(self, message: str) -> None:
        """Logs a debug message"""
        self.logger.debug(message)

    def warning(self, message: str) -> None:
        """Logs a warning message"""
        self.logger.warning(message)