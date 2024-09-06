import os

import requests
from pyrogram import Client, filters

from bot import logger
from bot.core import filters as fltr


@Client.on_message(filters.command("deploy", "build") & fltr.group("admin"))
async def build(client, message):
    logger.info("redeploying")
    build_url = os.environ.get("build_url", "")
    requests.post(build_url)
