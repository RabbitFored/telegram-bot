# Create and configure logger

import logging
from .TelegramLogger import tgHandler
from .FileLogger import fileHandler


root_logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format=
                    '[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# Initialize Logger
logger = logging.getLogger('tgbot')


#set log levels
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)

# File Handler with Rotation
root_logger.addHandler(fileHandler)

if tgHandler:
     root_logger.addHandler(tgHandler)
