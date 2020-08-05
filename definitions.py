# coding=utf-8
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Project root

TEMP_DIR = ROOT_DIR + '/temp'  # path to store system generated conf files
EXAMPLES_DIR = ROOT_DIR + '/examples'  # path to store example conf files

def create_dir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print('created directory %s: ', directory)



