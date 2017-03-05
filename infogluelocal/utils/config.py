import json
import os


config = {}

if not os.path.isfile('config.json'):
    print('config.json could not be found.')
else:
    config = json.loads('config.json')
