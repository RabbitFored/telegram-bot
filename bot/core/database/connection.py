#from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from ..shared import CONFIG


usercache_client = AsyncIOMotorClient(CONFIG.mongouri)
usercache_db = usercache_client['TELEGRAM']
usercache = usercache_db['usercache']

bot_client = AsyncIOMotorClient(CONFIG.mongouri)
bot_db = bot_client[CONFIG.database] 
botdata = bot_db['botdata']