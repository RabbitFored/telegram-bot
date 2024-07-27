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
for name in logging.root.manager.loggerDict:
    if myloggers.get(name, None):
        level = myloggers[name].get("level","INFO")
        logging.getLogger(name).setLevel(logging._nameToLevel[level.upper()])


root_logger = logging.getLogger()
level = myloggers["root"].get("level","INFO")
root_logger.setLevel(logging._nameToLevel[level.upper()])

