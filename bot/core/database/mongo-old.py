'''
from bson.objectid import ObjectId
from .. import utils
from datetime import datetime, timedelta
from cachetools import TTLCache

#from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from ..shared import CONFIG


usercache_client = AsyncIOMotorClient(CONFIG.mongouri)
usercache_db = usercache_client['TELEGRAM']
usercache = usercache_db['usercache']

bot_client = AsyncIOMotorClient(CONFIG.mongouri)
bot_db = bot_client[CONFIG.database] 
botdata = bot_db['botdata']

user_cache = TTLCache(maxsize=1000, ttl=60) 

async def get_user(userID):
  if userID in user_cache:
    return user_cache[userID]
    
  userinfo = await usercache.find_one(utils.make_filter(userID))
  if userinfo:
    objInstance = ObjectId(userinfo["_id"])
    userdata = await botdata.find_one({"user": objInstance})
    if userdata:
      user = utils.generate_user(userinfo, userdata)
      user_cache[userID] = user
      return user
    else:
      return None
  else:
    return None

async def init_userinfo(msg):
  userID = msg.from_user.id
  username = msg.from_user.username
  firstname = msg.from_user.first_name
  lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""
  dc = msg.from_user.dc_id if msg.from_user.dc_id else 0
  now = msg.date
  name = firstname + lastname
  userinfo = {
    "userid": userID,
    "name": [name],
    "username": [username],
    "dc": dc,
    #"is_banned": False,
    #"groups": [],
    #"enrolls": [1904425008],
    "firstseen": now,
    "lastseen": now
  }
  r = await usercache.insert_one(userinfo)
  return r

async def init_userdata(userObjectID, now):
  userdata = {
    "user": userObjectID,
  #  "status": "active",
  #  "is_banned": False,
  #  "warns": 0,
  #  "subscription": {
  #     "name": "free",
  #   },
  #  "data": {},
  #    "settings": {},
    "firstseen": now,
    "lastseen": now
  }
  r = await botdata.insert_one(userdata)
  return r
  
async def add_user(msg):
  userID = msg.from_user.id
  try:
    userinfo = await usercache.find_one(utils.make_filter(userID))
  except:
    userinfo = None

  if not userinfo:
    r = await init_userinfo(msg)
    userObjectID = ObjectId(r.inserted_id)
  else:
    userObjectID = ObjectId(userinfo["_id"])
  await init_userdata(userObjectID, msg.date)
  return True

async def update_lastseen(userID, lastseen):
  newvalues = {"$set": {"lastseen": lastseen}}
  
  userinfo = await usercache.find_one(utils.make_filter(userID))
  
  filter = {'user': ObjectId(userinfo['_id'])}
  await botdata.update_one(filter, newvalues)
  
async def update_user(userID, newvalues):
  userinfo = await usercache.find_one(utils.make_filter(userID))
  filter = {'user': ObjectId(userinfo['_id'])}
  await botdata.update_one(filter, newvalues)
  
  if userID in user_cache:
    del user_cache[userID]

async def update_user_info(userID,newvalues):
  await usercache.update_one(utils.make_filter(userID), newvalues )

async def fetch_all():
  userdata = await botdata.find({"status": {"$ne": "inactive"}}, {"_id": 0, 'user': 1 })
  object_ids = [ObjectId(user["user"]) for user in userdata]
  userinfo = await usercache.find({"_id": {"$in": object_ids}} , {"_id": 0, "userid": 1})
  userIDs = [u["userid"] for u in userinfo]
  return userIDs

async def data_exists(data):
  query = {f'data.{key}': value for key, value in data.items()}
  cursor = list((await botdata.find(query)))
  return bool(cursor)

async def find_data(data):
  query = {f'data.{key}': value for key, value in data.items()}
  userdata = await botdata.find_one(query)
  if userdata:
      userinfo = await usercache.find_one({'_id': ObjectId(userdata['user'])})
      user = utils.generate_user(userinfo, userdata)
      return user
  else:
      return None

async def update_user_data(userID, method, data):
  d = {f'data.{key}': value for key, value in data.items()}
  update_user(userID, { method :  d })

async def delete_user(userID):
  filter = utils.make_filter(userID)
  userinfo = await usercache.find_one(filter)
  if userinfo:
    objInstance = ObjectId(userinfo["_id"])
    await botdata.delete_one({"user": objInstance})
    await usercache.delete_one(filter)
    return True
  else:
    return False

async def statial(what,how):
  collection = bot_db["statial"]
  await collection.update_one( {}, {"$inc": { what : how }} )
  return "ok"

async def get_statial():
  collection = bot_db["statial"]
  value = await collection.find_one()
  return value

async def get_active_users():
  total_users = await botdata.count_documents({})
  active_users = await botdata.count_documents({
      'lastseen': {'$gte': datetime.now() - timedelta(days=7)}
  })

  return {
      'total_users': total_users,
      'active_users': active_users
  }
  '''