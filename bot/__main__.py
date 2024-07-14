from . import bot, CONFIG, logger
from .core import filters as fltr
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from . import strings
import os

#check users in banlist and forcesub
@bot.on_message(fltr.user_filter)
async def user_check(client, message):
    channel_url = CONFIG.settings["links"]["channel_url"]
    text = strings.FORCE_SUB_TEXT.format(channel=f"@{channel_url.split('/')[-1]}")
    keyboard = [
        [
            InlineKeyboardButton("Subscribe", url=channel_url),
        ]
    ]
    await message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard),
        quote=True,
    )


if __name__ == "__main__":
    webfile = os.path.dirname(__file__) + "/plugins/web.py"
    if CONFIG.settings["web"] == True and os.path.isfile(webfile): 
        from mailable.plugins.web import app
        logger.info("Starting web client and bot")
        bot.start()
        app.run("0.0.0.0", CONFIG.port, loop=bot.loop)
    else:
        logger.info("Starting bot")
        bot.run()
