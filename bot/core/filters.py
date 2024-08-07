import json

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

from ..core import antiflood, logger
from ..core import database as db
from ..core.shared import CONFIG


async def user_check(_, c, msg):
  #if msg.chat.type:
  
  #set self
  if not CONFIG.me:
    CONFIG.me = await c.get_me()
  
  if msg.chat.type != ChatType.PRIVATE:
    return False
  
  json_object = json.loads(f"{msg}")
  instance = json_object["_"]

  if instance == "Message":
    userID = msg.chat.id
  elif instance == "CallbackQuery":
    userID = msg.message.chat.id
  elif instance == "InlineQuery":
    userID = msg.from_user.id
  else:
    logger.warn(instance)
    return False

  #allow self without filters
  if userID == CONFIG.me.id:
    return False
  
  #allowed groups and subscribers
  allowed_groups = CONFIG.settings["filters"]["exclude"].get("groups", [])
  allowed_subscriptions = CONFIG.settings["filters"]["exclude"].get("subscriptions", [])

  allowed_users = []
  for group in allowed_groups:
    allowed_users.extend(CONFIG.settings["groups"][group])
    
  if userID in allowed_users:
    return False
    
  user = db.get_user(userID)
  
  if not user:
    db.add_user(msg)
  else:
    user.refresh(msg)
    if bool(user.is_banned):
      return True

  if user.subscription["name"] in allowed_subscriptions:
    return False

  
  if antiflood and antiflood.is_flooding(userID):
    user.warn()
    antiflood.flush_user(userID)
    return
  
  user_pass = False
  

  if bool(CONFIG.settings["fliters"]["force_sub"]):
    chat = CONFIG.settings["fliters"]["force_sub"].get("chats")[0]
    try:
      await c.get_chat_member(chat, userID)
      user_pass = True
    
    except UserNotParticipant:
      user_pass = False
    except ChatAdminRequired:
      logger.error("Chat Admin Permission Required to perform this function")
      return False
  else:
    user_pass = True

  if not user_pass:
    return True
    
  return False


class group(filters.Filter, set):
   def __init__(self, groups):
     self.groups = [] if groups is None else self.groups if isinstance(groups, list) else [groups]

   async def __call__(self, _, message):
     return bool(CONFIG.in_group(message.from_user.id, self.groups[0]))



user_filter = filters.create(user_check)


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
  
  return filters.command(commands, prefixes,case_sensitive=case_sensitive)