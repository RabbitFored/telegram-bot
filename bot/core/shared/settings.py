import os

import yaml

DEV = bool(os.environ.get('DEV', False)) and os.environ.get('DEV', False) != 'False'

settings_path = 'settings-dev.yaml' if DEV else 'settings.yaml'

with open(settings_path, "r") as settings_file:
  settings = yaml.safe_load(settings_file)

#TODO