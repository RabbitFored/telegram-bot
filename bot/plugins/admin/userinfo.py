from pyrogram import Client, filters

from bot.core import database as db
from bot.core import filters as fltr
from bot.core import utils


@Client.on_message(filters.command(["user"]) & fltr.group("admin"))
async def user(client, message):
    user = await db.get_user(utils.get_user(message))

    if not user:
        await message.reply_text("**No user found!**")
        return
    text = f"""
**User:** {user.name}
**ID:** {user.ID}
**Username:** @{user.username}
**DC:** `{user.dc}`
**First seen:** `{user.firstseen}`
**Last seen:** `{user.lastseen}`
**Warns:** `{user.warns}`
**Banned:** `{user.is_banned}`
**Subscription:** `{user.subscription}`
"""
    await message.reply_text(text)
