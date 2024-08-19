# Create and configure logger
import logging

from ..shared import CONFIG
from .handlers import handlers

logging.basicConfig(
    level=logging.INFO,
    format=
    '[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')

# Initialize tgbot logger
logger = logging.getLogger('tgbot')

root_logger = logging.getLogger()

#set levels
myloggers = CONFIG.settings["logging"]["loggers"]

for col in myloggers:
    names = col.split(",")
    for name in names:
        name = name.strip()
        tlogger = logging.getLogger(name)
        
        #Set level
        tlevel = myloggers[col].get("level","INFO")
        tlogger.setLevel(logging._nameToLevel[tlevel.upper()])

        #Set handlers    
        thandlers = myloggers[col].get("handlers", [])
        for thandler in thandlers:
            thandler = thandler.strip()
            if thandler in handlers:
                tlogger.addHandler(handlers[thandler])
            else:
                root_logger.warn("Skipping Unknown handler: %s", thandler)
            