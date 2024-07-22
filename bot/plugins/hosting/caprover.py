import os
from pyrogram import Client, filters
from bot.core import filters as fltr
from bot import logger
import requests


@Client.on_message(filters.command("deploy", "build") & fltr.group("admin"))
async def build(client, message):
    logger.info("redeploying")
    build_token = os.environ.get("caprover_build_token","")
    build_url = f"https://captain.theostrich.eu.org/api/v2/user/apps/webhooks/triggerbuild?namespace=captain&token={build_token}"
    requests.post(build_url)