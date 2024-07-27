import json

from pyrogram import filters
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pyrogram.enums import ChatType
from ..core import database as db
from ..core.shared import CONFIG
from ..core import logger

async def user_check(_, c, msg):
  #if msg.chat.type:
  if not msg.chat.type== ChatType.PRIVATE:
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
    print(instance)

  user = db.get_user(userID)

  if not user:
    db.add_user(msg)
  else:
    user.refresh(msg)
    if bool(user.is_banned):
      return True
  
  user_pass = False

  if bool(CONFIG.settings["force_sub"]):
    try:
      chat = CONFIG.settings["FORCE_SUB_CHANNEL"]
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