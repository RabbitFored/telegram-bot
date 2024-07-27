# Create and configure logger

import logging

from ..shared import CONFIG

# Initialize Logger
logger = logging.getLogger('tgbot')


root_logger = logging.getLogger()
print(root_logger.handlers)
level = CONFIG.settings["logs"]["log_level"]

if level.upper() not in logging._nameToLevel:
    logger.info("Invalid log level: " + level)
    level = "INFO"

logging.basicConfig(
    level=logging._nameToLevel[level.upper()],
    format=
    '[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
logger.info("Setting log level to: " + level.upper())


#set log levels
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)



