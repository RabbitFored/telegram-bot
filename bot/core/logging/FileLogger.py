import logging
import os
from logging.handlers import RotatingFileHandler
from ..shared import CONFIG

units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}

def get_bytes(size):
   number, unit = [string.strip() for string in size.split()]
   return int(float(number)*units[unit])

formatter = logging.Formatter(
'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_logger = CONFIG.settings["logs"]["file"]
if CONFIG.settings["logs"]["file"]:
   root_logger = logging.getLogger()
   
   dir = file_logger.get("dir", "logs")
   if not os.path.exists(dir):
      os.makedirs(dir)
   filename = os.path.join(dir, file_logger.get("filename","bot.log"))
   maxBytes = get_bytes(file_logger.get("maxSize", "1 MB"))
   backupCount = int(file_logger.get("backupCount", 5))
   
   
   fileHandler = RotatingFileHandler(filename,
      maxBytes=maxBytes,
         backupCount=backupCount)
  #fileHandler.setLevel(logging.INFO)
   fileHandler.setFormatter(formatter)
   root_logger.addHandler(fileHandler)
