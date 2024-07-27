from pyrogram import Client, filters
from bot.core import utils
from bot.core import database as db
from bot.core import filters as fltr

@Client.on_message(filters.command(["statial"])  & fltr.group("admin") )
async def statial(client, message):
       stat = db.get_statial()
       users = db.bot_db["botdata"].count_documents({})
       text = "**Statial**\n\n"
       text += f"**Total Users:** {users}\n"                                
       for i in stat:
           if not i == "_id":
             text += f"**{i}:** {stat[i]}\n" 
       await message.reply_text(text)