from pyrogram import Client, filters
from bot.core import utils
from bot.core import database as db
from bot.core import filters as fltr

@Client.on_message(filters.command(["ban"])  & fltr.group("admin") )
async def ban(client, message):
  userID = utils.get_user(message)
  if not userID:
    await message.reply_text("**No user found!**")
    return
  user = db.get_user(userID)
  user.ban()
  await message.reply_text(f"Banned {userID}")

@Client.on_message(filters.command(["unban"])  & fltr.group("admin") )
async def unban(client, message):
  userID = utils.get_user(message)
  if not userID:
    await message.reply_text("**No user found!**")
    return
  user = db.get_user(userID)
  user.unban()
  await message.reply_text(f"Unbanned {userID}")

@Client.on_message(filters.command(["clear_warns"])  & fltr.group("admin") )
async def clear_warns(client, message):
  userID = utils.get_user(message)
  if not userID:
    await message.reply_text("**No user found!**")
    return
  user = db.get_user(userID)
  user.clear_warns()
  await message.reply_text(f"Cleared all warnings for {userID}")
