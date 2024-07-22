import os
from pyrogram import Client, filters
from bot.core import filters as fltr
from bot import logger
import requests


@Client.on_message(filters.command("deploy", "build") & fltr.group("admin"))
async def build(client, message):
    logger.info("redeploying")
    requests.post(os.environ['caprover_build_token'])