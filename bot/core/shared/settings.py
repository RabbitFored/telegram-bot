import yaml

settings_path = "settings.yaml"

settings_file = open(settings_path, "r")
settings = yaml.safe_load(settings_file)

#TODO