from pyrogram import Client, filters

from bot.core import database as db
from bot.core import filters as fltr
from bot.core import utils


@Client.on_message(filters.command(["ban"])  & fltr.group("admin") )
async def ban(client, message):
  userID, username = utils.get_target_user(message)
  user = await db.get_user(userID, username, fetch_info=True)

  if not user:
      await message.reply_text("**No user found!**")
      return
    
  await user.ban()
  await message.reply_text(f"Banned {userID}")

@Client.on_message(filters.command(["unban"])  & fltr.group("admin") )
async def unban(client, message):
  userID, username = utils.get_target_user(message)
  user = await db.get_user(userID, username, fetch_info=True)

  if not user:
      await message.reply_text("**No user found!**")
      return
    
  await user.unban()
  await message.reply_text(f"Unbanned {userID}")

@Client.on_message(filters.command(["clear_warns"])  & fltr.group("admin") )
async def clear_warns(client, message):
  userID, username = utils.get_target_user(message)
  user = await db.get_user(userID, username, fetch_info=True)

  if not user:
      await message.reply_text("**No user found!**")
      return

  await user.clear_warns()
  await message.reply_text(f"Cleared all warnings for {userID}")
