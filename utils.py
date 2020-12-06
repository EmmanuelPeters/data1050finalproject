'''This module contains the utility functions used by other modules'''
import sys
import time
import logging

def setup_logger(logger, output_file):
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter('%(asctime)s [%(funcName)s]: %(message)s'))
    logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler(output_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(funcName)s] %(message)s'))
    logger.addHandler(file_handler)

def ymdhms(delimiter='-'):
    '''Generate a time stamp with the formate yyyy-mm-dd-hh-mm-ss'''
    t = time.localtime()
    t = [str(i) for i in t[:6]]
    return delimiter.join(t)