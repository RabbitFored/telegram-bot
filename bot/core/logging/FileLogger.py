import logging
import os
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter(
'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

try:
   fileHandler = RotatingFileHandler('logs/bot.log',
   maxBytes=1 * 1024 * 1024,
   backupCount=5)
except FileNotFoundError:
   os.mkdir("logs/")
   fileHandler = RotatingFileHandler('logs/bot.log',
      maxBytes=1 * 1024 * 1024,
      backupCount=5)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)