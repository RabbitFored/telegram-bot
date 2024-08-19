import json
from .. import strings
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from ..core.utils import generate_keyboard
from ..core import antiflood, logger
from ..core import database as db
from ..core.shared import CONFIG
import time

async def user_check(_, c, msg):
  
  #if msg.chat.type: TODO

  #make checks only for private chats
  if msg.chat.type != ChatType.PRIVATE:
    return False

  userID = msg.from_user.id

  
  
  #allow self
  if userID == CONFIG.me.id:
    return False

  

  user = await db.get_user(userID)
  
  #add new user to db
  if not user:
    await db.add_user(msg)
  else:
    if bool(user.is_banned):
      return await msg.reply("You are banned from using this bot.")
    await user.refresh(msg)
    
  
  #allowed groups and subscribers
  allowed_groups = CONFIG.settings["filters"]["exclude"].get("groups", [])
  allowed_subscriptions = CONFIG.settings["filters"]["exclude"].get(
      "subscriptions", [])

  allowed_users = []
  for group in allowed_groups:
    allowed_users.extend(CONFIG.settings["groups"][group])

  if userID in allowed_users:
    return False

  if user and user.subscription.get("name", "free") in allowed_subscriptions:
    return False

  #warn flooding users
  if antiflood and antiflood.is_flooding(userID):
    await user.warn()
    antiflood.flush_user(userID)
    return await msg.reply(
        "You are flooding me, slow down!\n\nFlooding may cause your account to be banned."
    )

  #force sub
  if bool(CONFIG.settings["filters"].get("force_sub", None)):
    chat = CONFIG.settings["filters"]["force_sub"].get("chats")[0]
    try:
      await c.get_chat_member(chat, userID)
    except UserNotParticipant:
      channel_url = CONFIG.settings["links"]["channel_url"]

      text = strings.get("force_sub_txt",
                         channel=f"@{channel_url.split('/')[-1]}")
      keyboard = generate_keyboard(
          strings.get("force_sub_btn", channel_url=channel_url))

      return await msg.reply(
          text,
          disable_web_page_preview=True,
          reply_markup=keyboard,
          quote=True,
      )
    except ChatAdminRequired:
      logger.error("Chat Admin Permission Required to perform this function")
      return False
  else:
    return False
  return False


class group(filters.Filter, set):

  def __init__(self, groups):
    self.groups = [] if groups is None else self.groups if isinstance(
        groups, list) else [groups]

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

  return filters.command(commands, prefixes, case_sensitive=case_sensitive)
