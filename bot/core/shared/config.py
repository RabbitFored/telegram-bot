import os

import yaml
from dotenv import load_dotenv

load_dotenv()

settings_path = "settings.yaml"
settings_file = open(settings_path, "r")


class config:
  def __init__(self):
    self.apiID = os.environ.get("apiID", None)
    self.apiHASH = os.environ.get("apiHASH", None)
    self.botTOKEN = os.environ.get("botTOKEN", None)
    self.session_string = os.environ.get("sessionString", None)
    self.mongouri = os.environ.get("MONGOURI", "")
    self.baseURL = os.environ.get("baseURL", "")
    self.port = int(os.environ.get("PORT", 5000))
    self.database = os.environ.get("DATABASE", "telegrambot")
    self.settings = yaml.safe_load(settings_file)
    self.me = None
  def get_group(self,group):
    groups = self.settings["groups"]
    users = groups[group]
    return users

  def in_group(self, userID, group):
    users = self.get_group(group)
    return userID in users


