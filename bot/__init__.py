import sys
from quart import Quart
from pyrogram import Client
from quart import Quart, send_file, render_template
from .core import ProcessManager, logger
from .core.shared import CONFIG
from .core import Translator
import os
import tempfile 

#if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

# setting up processes
ProcessManager = ProcessManager()

# Initialize bot
bot = Client("bot", api_id=CONFIG.apiID, api_hash=CONFIG.apiHASH, bot_token=CONFIG.botTOKEN, plugins= dict(root="bot/plugins"), alt_port=True)
web = Quart(__name__,template_folder='../public')

@web.route('/')
async def index():
    return await render_template("index.html")
    
# Initialize strings
default_language = CONFIG.settings["translation"]["default_language"]
lang_dir = CONFIG.settings["translation"]["dir"]

strings = Translator(dir=lang_dir, default_language=default_language)

#make temp dir
try:
    os.makedirs("/tmp/bot", exist_ok=True)
    tempfile.tempdir = "/tmp/bot"
    print("Directory created successfully")
except OSError as error:
    print("Directory can not be created")
