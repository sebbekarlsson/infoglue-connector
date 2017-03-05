import json
import os


config = {}

if not os.path.isfile('config.json'):
    print('config.json could not be found.')
else:
    with open('config.json') as config_file:
        config_text = config_file.read()
    config_file.close()

    config = json.loads(config_text)
