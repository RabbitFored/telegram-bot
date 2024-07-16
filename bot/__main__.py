from . import bot, CONFIG, logger
from .core import filters as fltr
from bot.core.utils import generate_keyboard
from bot import strings
from pyrogram import filters
import os


#check users in banlist and forcesub
@bot.on_message(fltr.user_filter)
async def user_check(client, message):

    channel_url = CONFIG.settings["links"]["channel_url"]

    text = strings.get("force_sub_txt",
                       channel=f"@{channel_url.split('/')[-1]}")
    keyboard = generate_keyboard(
        strings.get("force_sub_btn", channel_url=channel_url))

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=keyboard,
        quote=True,
    )


if __name__ == "__main__":
    
    if True:
        from . import web
        logger.info("Starting web client and bot")
        bot.start()
        web.run("0.0.0.0", CONFIG.port, loop=bot.loop)
    else:
        logger.info("Starting bot")
        bot.run()
