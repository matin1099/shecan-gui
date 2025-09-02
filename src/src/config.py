from loguru import logger as log
import configparser

import os
import sys


def config_reader():
    config = configparser.ConfigParser()
    config.read('FILE.INI')


def config_writer():
    log.info('Creating new config file...')
    data_list =  {
        'default_shecan':{
        'dns': '178.22.122.100',
        'alt_dns': '185.51.200.2'}}
    data_str = json.dumps(data_list, indent=4)
    with open('setting_shecanConfig.json', 'w') as f:
        f.write(data_str)
    log.success('Config file created. with public shecan DNS')


def config_add(data_list):
    """
    to add profile to json
    :param data_list: list contain of 3 array
    it must be [profile name, dns, alt_dns]
    :return: add new config to json
    """
    pass

def config_remove(profile_name:str):
    """
    remove profile from json
    :param profile_name:
    :return: json WITHOUT profile name
    """
    pass