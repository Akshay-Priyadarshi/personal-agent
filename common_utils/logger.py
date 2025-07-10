import logging
import time

from datetime import UTC, datetime
from enum import Enum

from pythonjsonlogger.jsonlogger import JsonFormatter


class UTCJsonFormatter(JsonFormatter):
    """Custom JSON formatter that adds UTC timestamp to log records.

    Extends the JsonFormatter class to automatically include a 'created' field
    with UTC ISO formatted datetime string in all log records. The timestamp
    is formatted as ISO 8601 with 'Z' suffix instead of '+00:00'.
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # Add UTC ISO formatted datetime string
        log_record['created'] = (
            datetime.now(tz=UTC).isoformat().replace('+00:00', 'Z')
        )


class LoggerUtils:
    """Utility class for logging operations.

    Provides methods to handle application logging with context and formatting.
    """

    class LogLevel(Enum):
        """Enumeration of standard logging levels.
        Defines the standard logging levels used throughout the application,
        mapping to the corresponding numeric values used by Python's logging
        module.

        Attributes:
            NOTSET (int): 0 - All messages are processed
            DEBUG (int): 10 - Detailed information for debugging
            INFO (int): 20 - General information messages
            WARNING (int): 30 - Warning messages for potential issues
            ERROR (int): 40 - Error messages for serious problems
            CRITICAL (int): 50 - Critical error messages for fatal issues
        """

        NOTSET = 0
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50

    @staticmethod
    def get_logger(
        name: str,
        level: LogLevel = LogLevel.DEBUG,
        file_path: str = './app.log',
    ) -> logging.Logger:
        """Get a logger instance with the specified name and level.

        Args:
            name (str): The name of the logger. Used to identify the logger
                instance and typically corresponds to the module or component
                name where the logger is used.
            level (LogLevel, optional): The logging level for the logger.
                Defaults to LogLevel.DEBUG. Controls which log messages are
                processed and output.
            file_path (str): The file path where log messages will be written.
                Defaults to './app.log'. Specifies the location of the log file
                for file-based logging output.

        Returns:
            logging.Logger: A configured logger instance with:
                - UTC timezone formatting
                - JSON output format with metadata
                - Stream handler for console output
                - Custom formatter including file name,
                  function name, and line number

        Example:
            >>> logger = LoggerUtils.get_logger('my_module')
            >>> logger.debug('Application started')
        """
        logger = logging.getLogger(name)

        # Clear any existing handlers to avoid duplicates
        logger.handlers.clear()

        # Ensure propagation is enabled
        logger.propagate = False

        logger.setLevel(level=level.value)

        logger.addHandler(LoggerUtils.get_file_handler(file_path=file_path))
        logger.addHandler(LoggerUtils.get_stdout_handler())
        return logger

    @staticmethod
    def get_file_handler(file_path: str) -> logging.FileHandler:
        handler = logging.FileHandler(filename=file_path)

        # Custom UTCJsonFormatter with additional fields and UTC timezone
        formatter = UTCJsonFormatter(
            fmt=(
                '%(levelname)s %(name)s %(module)s %(filename)s %(funcName)s%(lineno)d %(process)d %(thread)d %(message)s'
            ),
            datefmt='%Y-%m-%d %H:%M:%S',
            json_indent=2,
        )
        formatter.converter = lambda *args: time.gmtime()
        handler.setFormatter(fmt=formatter)
        return handler

    @staticmethod
    def get_stdout_handler() -> logging.StreamHandler:
        handler = logging.StreamHandler()

        # Custom UTCJsonFormatter with additional fields and UTC timezone
        formatter = UTCJsonFormatter(
            fmt=(
                '%(levelname)s %(name)s %(module)s %(filename)s %(funcName)s%(lineno)d %(process)d %(thread)d %(message)s'
            ),
            datefmt='%Y-%m-%d %H:%M:%S',
            json_indent=2,
        )
        formatter.converter = lambda *args: time.gmtime()
        handler.setFormatter(fmt=formatter)
        return handler
