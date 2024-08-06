import logging
import os
from logging.handlers import RotatingFileHandler
from ...shared import CONFIG

units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}

def get_bytes(size):
   number, unit = [string.strip() for string in size.split()]
   return int(float(number)*units[unit])

formatter = logging.Formatter(
'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_logger = CONFIG.settings["logging"]["handlers"]["file"]
if file_logger:
   root_logger = logging.getLogger()
   path = file_logger.get("path", "logs/bot.log")
   dir, filename  =  os.path.split(path)

   if not os.path.exists(dir):
      os.makedirs(dir)

   maxBytes = get_bytes(file_logger.get("maxSize", "1 MB"))
   backupCount = int(file_logger.get("backupCount", 5))
   tlevel = file_logger.get("level", "DEBUG")

   fileHandler = RotatingFileHandler(path,
      maxBytes=maxBytes,
         backupCount=backupCount)
   fileHandler.setLevel(logging._nameToLevel[tlevel.upper()])
   fileHandler.setFormatter(formatter)
else:
   fileHandler = None