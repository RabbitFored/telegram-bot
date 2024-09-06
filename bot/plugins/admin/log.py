import logging
import os

from pyrogram import Client, filters
from pyrogram.types import InputMediaDocument

from bot import logger
from bot.core import filters as fltr


@Client.on_message(filters.command("set_loglevel") & fltr.group("admin"))
async def set_log_level(client, message):
    _, level = message.text.split()
    level = level.upper()
    if level in logging._nameToLevel:
        logger.setLevel(logging._nameToLevel[level])
        await message.reply(f"Log level set to {level}")
    else:
        await message.reply("Invalid log level")


@Client.on_message(filters.command(["logs", "get_logs"]) & fltr.group("admin"))
async def get_logs(client, message):
    LOG_DIR = "logs"
    log_files = [
        InputMediaDocument(os.path.join(LOG_DIR, f))
        for f in sorted(os.listdir(LOG_DIR))
        if f.startswith("bot.log")
    ]

    if not log_files:
        await message.reply("No log files found.")
        return
    m = await message.reply("Sending log files, Please wait...")

    await message.reply_media_group(log_files)
    await m.delete()
    await message.reply("All log files have been sent.")
