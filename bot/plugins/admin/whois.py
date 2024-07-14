from pyrogram import Client, filters
from bot.core import database as db
from bot.core import filters as fltr

@Client.on_message(filters.command(["whois"]) & fltr.group("admin") )
async def whois(client, message):
  args = message.text.split(" ")

  mailID = args[1]
  data = {"mails": mailID.lower()}
  user = db.find_data(data)

  await message.reply_text(f'Mail {mailID} belongs to `{user.ID}`')



