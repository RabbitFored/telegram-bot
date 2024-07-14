from pyrogram import Client, filters
from bot.core import utils
from bot.core import database as db
from bot.core import filters as fltr

@Client.on_message(filters.command(["user"])  & fltr.group("admin") )
async def user(client, message):
  userID = utils.get_user(message)
  user = db.user.get(userID)

  if not user:
    await message.reply_text("**No user found!**")
    return
  text = f'''
**User:** {user.name}
**Username:** @{user.username}
**DC:** `{user.dc}`
**First seen:** `{user.firstseen}`
**Last seen:** `{user.lastseen}`
**Banned:** `{user.is_banned}`
**Subscription:** `{user.subscription}`
'''

  await message.reply_text(text)