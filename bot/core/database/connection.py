from pymongo import MongoClient
from ..shared import CONFIG


usercache_client = MongoClient(CONFIG.mongouri)
usercache_db = usercache_client['TELEGRAM']
usercache = usercache_db['usercache']

bot_client = MongoClient(CONFIG.mongouri)
bot_db = bot_client[CONFIG.database] 
botdata = bot_db['botdata']