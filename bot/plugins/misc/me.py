from pyrogram import Client, filters
from bot.core import database as db

@Client.on_message(filters.command(["me"]) )
async def me(client, message):
  user = db.get_user(message.from_user.id)

  text = f'''
**User:** {user.name}
**ID:** {user.ID}
**Username:** @{user.username}
**Warns:** `{user.warns}`

**Subscription:** `{user.subscription["name"].upper()}`
'''
  if user.subscription.get("name") != "free":
    expiry = user.subscription["expiry_date"]
    text += f"**Expiry:** `{expiry.strftime('%Y-%m-%d')}`"
  await message.reply_text(text, quote =True)