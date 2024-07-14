from pyrogram import Client, filters
from bot import strings, CONFIG
from bot.core.utils import generate_keyboard
from bot.core import database as db

@Client.on_message(filters.command(["start"]))
async def start(client, message):

    text = strings.START_TEXT.format(user=message.from_user.mention)
    keyboard = generate_keyboard(strings.START_BTN)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        reply_markup=keyboard,
        quote=True,
    )


@Client.on_message(filters.command(["help"]))
async def get_help(client, message):
    text = strings.HELP_TEXT
    keyboard = generate_keyboard(strings.HELP_BTN)

    # extended help message for bot administrator
    chatID = message.chat.id
    admins = CONFIG.get_group("admin")

    if chatID in admins:
        text += strings.ADMIN_HELP_TEXT
    if message.from_user.is_self:
        await message.edit(text,
                           reply_markup=keyboard,
                           disable_web_page_preview=True)
    else:
        await message.reply_text(text,
                             reply_markup=keyboard,
                             quote=True,
                             disable_web_page_preview=True)


@Client.on_message(filters.command(["about"]))
async def aboutTheBot(client, message):
    text = strings.ABOUT_TEXT
    keyboard = generate_keyboard(strings.ABOUT_BTN)

    await message.reply_text(text,
                             reply_markup=keyboard,
                             quote=True,
                             disable_web_page_preview=True)


@Client.on_message(filters.command(["donate"]))
async def donate(client, message):
    text = strings.DONATE_TEXT
    keyboard = generate_keyboard(strings.DONATE_BTN)

    await message.reply_text(text,
                             reply_markup=keyboard,
                             quote=True,
                             disable_web_page_preview=True)


@Client.on_message(filters.command(["sponsors"]))
async def sponsors(client, message):
    text = strings.SPONSORS_TEXT
    await message.reply_text(text, 
                             quote=True, 
                             disable_web_page_preview=True)

@Client.on_message(filters.command(["me"]))
async def user_info(client, message):
  user = db.get_user(message.from_user.id)

  text = f'''
**ID:** {user.ID}
**User:** {user.name}
**Username:** @{user.username}
**First seen:** `{user.firstseen}`
**Last seen:** `{user.lastseen}`
'''
  data = f'''
**Mails:** `{user.data.get("mails", "")}`
**Blocks:** `{user.data.get("blocks", "")}`
   '''
  text += data
  await message.reply_text(text)
