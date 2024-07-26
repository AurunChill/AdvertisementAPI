import logging
from logging.handlers import RotatingFileHandler

from config import settings


def create_log_files_if_not_exist():
    """
    Creates the log directory if it does not already exist.

    This function checks the specified log path in the settings. If the directory 
    does not exist, it creates the necessary directories to ensure that log files 
    can be saved without error.
    """
    log_settings = settings.log
    if not log_settings.LOG_PATH.exists():
        log_settings.LOG_PATH.mkdir(parents=True)


def setup_logger(logger_name: str, filename: str = 'app.log'):
    """
    Sets up a logger with a file handler that rotates logs.

    This function configures a logger with a specified name, setting its level 
    to DEBUG. If the log files do not exist, it creates them. It also configures 
    a rotating file handler that limits the size of the log file and keeps a 
    backup count of previous log files.

    Args:
        logger_name (str): The name of the logger to be created
        filename (str, optional): The name of the log file. Defaults to 'app.log'.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    log_settings = settings.log

    create_log_files_if_not_exist()

    if not (log_settings.LOG_PATH / filename).exists():
        (log_settings.LOG_PATH / filename).touch()
        
    file_handler = RotatingFileHandler(filename=log_settings.LOG_PATH / filename, maxBytes=5*1024*1024, backupCount=2)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def clear_log_files():
    """
    Clears all log files in the specified log directory.

    Parameters:
        None

    Returns:
        None
    """
    log_settings = settings.log
    for file in log_settings.LOG_PATH.glob('*.log'):
        with open (file, 'w') as f:
            f.write('')


clear_log_files()
app_logger = setup_logger(logger_name='AppLogger')
db_query_logger = setup_logger(logger_name='DBQueryLogger', filename='db.log')
celery_logger = setup_logger(logger_name='CeleryLogger', filename='celery.log')
test_logger = setup_logger(logger_name='TestLogger', filename='test.log')
