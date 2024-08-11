from pyrogram import Client, filters
from bot.core import database as db
from bot.core import filters as fltr
from bot.core.utils import generate_keyboard
from bot import strings, logger, CONFIG
from bot.core import utils


@Client.on_message(filters.command(["gift"]) & fltr.group("admin"))
async def gift(client, message):
    userID = utils.get_user(message)
    if not userID:
        await message.reply_text("**No user found!**")
        return
    user = await db.get_user(userID)
    await user.gift("premium", message.from_user.id)
    await client.send_message(
        chat_id=user.ID,
        text=f"""
**Congratulations!**   

You got premium subscription for @{CONFIG.me.username} for a month.
   """,
    )
    await message.reply(f"Gifted premium for user {user.ID}")
