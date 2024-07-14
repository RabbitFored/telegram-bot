# Create and configure logger

import logging
from .TelegramLogger import tgHandler
from .FileLogger import fileHandler


# Initialize Logger
logger = logging.getLogger('tgbot')

logging.basicConfig(level=logging.INFO,
                    format=
                    '[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

#set log levels
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)

# File Handler with Rotation
logger.addHandler(fileHandler)

if tgHandler:
   logger.addHandler(tgHandler)
