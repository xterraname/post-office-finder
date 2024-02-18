import json
import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

with open(ROOT_DIR + '/config.json') as config_data:
    CONFIG = json.load(config_data)


def get_token(mode="local"):

    return CONFIG['bot'][mode]['token']