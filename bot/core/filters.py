from pyrogram import filters
from ..core.shared import CONFIG

#async def user_check(_, c, msg):
  
  #if msg.chat.type: TODO

#  userID = msg.from_user.id

  
  
  #allow self

    
  
  #allowed groups and subscribers
#  allowed_groups = CONFIG.settings["filters"]["exclude"].get("groups", [])
#  allowed_subscriptions = CONFIG.settings["filters"]["exclude"].get(
#      "subscriptions", [])
#
#  allowed_users = []
#  for group in allowed_groups:
#    allowed_users.extend(CONFIG.settings["groups"][group])
#
#  if userID in allowed_users:
#    return False
#
#  if user and user.subscription.get("name", "free") in allowed_subscriptions:
#    return False



class group(filters.Filter, set):
  def __init__(self, groups):
    self.groups = [] if groups is None else self.groups if isinstance(
        groups, list) else [groups]

  async def __call__(self, _, message):
    return bool(CONFIG.in_group(message.from_user.id, self.groups[0]))


#user_filter = filters.create(user_check)

def on_data(data):

  async def func(flt, _, query):
    return flt.data == query.data

  return filters.create(func, data=data)


def on_marker(data):

  async def func(flt, _, query):
    d = query.data.split("_")[0]
    return flt.data == d

  return filters.create(func, data=data)


def cmd(commands):
  prefixes = CONFIG.settings["commands"]["prefix"]
  case_sensitive = CONFIG.settings["commands"]["case_sensitive"]

  return filters.command(commands, prefixes, case_sensitive=case_sensitive)
