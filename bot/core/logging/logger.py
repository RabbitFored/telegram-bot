# Create and configure logger

import logging

from ..shared import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format=
    '[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

# Initialize tgbot logger
logger = logging.getLogger('tgbot')

#set levels
myloggers = CONFIG.settings["logging"]["loggers"]

for col in myloggers:
    names = col.split(",")
    for name in names:
        name = name.strip()
        level = myloggers[col].get("level","INFO")
        logging.getLogger(name).setLevel(logging._nameToLevel[level.upper()])
