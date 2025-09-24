"""
Configuration of the logging module for the entire project. Writes logs into a text file in the logs folder.
"""

import logging
from os.path import dirname, abspath, join, exists
from os import mkdir

def setup_logging():
    
    PARENT_FOLDER = dirname(dirname(abspath(__file__)))
    LOGS_FOLDER = join(PARENT_FOLDER, 'logs')
    if not exists(LOGS_FOLDER):
        mkdir(LOGS_FOLDER)

    logging.basicConfig(
        filename=join(LOGS_FOLDER, 'logging.txt'),
        level=logging.DEBUG,
        format='%(asctime)s -  %(levelname)s -  %(message)s',
        encoding='utf-8'
    )