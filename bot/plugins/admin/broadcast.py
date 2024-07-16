#from mailable import logger, CONFIG, PROCESSES
from pyrogram import filters, Client
import time
from bot.core import database as db
from bot.core import filters as fltr
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import ProcessManager, CONFIG
import asyncio

async def bcast(mode, msg,x,failed):
    users = db.fetch_all()
    
    for user in users:
        try:
            if mode == "copy":
                await msg.copy(user)
            else:
                await msg.forward(user)

                x += 1
                await asyncio.sleep(2)

        except:
                failed += 1 

@Client.on_message(filters.command(["broadcast"]) & fltr.group("admin"))
async def broadcast(client, message):
        processes = ProcessManager.list_processes()
        for p in processes:
            if p.name == 'broadcast':
                await message.reply_text("Another broadcast is already in progress. Please try again later.")
                return
        
        broadcast_msg = message.reply_to_message
        if not broadcast_msg:
            await message.reply(
                "Please reply to a message to broadcast it.", quote=True
            )
            return
            
        

        keyboard = [
            [
                InlineKeyboardButton("Check Progress", callback_data="ps_broadcast"),
            ]
        ]
        await message.reply_text("Broadcasting...",                                                    reply_markup=InlineKeyboardMarkup(keyboard))

        #PROCESSES.broadcast["status"] = True
        #PROCESSES.broadcast["total"] = len(users)
    
        #failed = 0
        #x = 0
    
        mode = CONFIG.settings["broadcast"]["mode"]
        if len(message.text.split(" ")) > 1:
            mode = message.text.split(" ")[1]
        process = ProcessManager.create_process("broadcast")
        process.data["x"] = 0
        process.data["failed"] = 0
        await process.start(bcast(mode,broadcast_msg,x=process.data["x"],failed=process.data["failed"]))  
    
