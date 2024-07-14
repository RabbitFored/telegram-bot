from logging.handlers import RotatingFileHandler
import logging 

formatter = logging.Formatter(
'%(asctime)s - %(name)s - %(levelname)s - %(message)s')


fileHandler = RotatingFileHandler('logs/bot.log',
   maxBytes=1 * 1024 * 1024,
   backupCount=5)
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)