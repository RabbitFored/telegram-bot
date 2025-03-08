#famini

from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

from .. import utils
from ..shared import CONFIG
from .base import BaseDatabase


class MongoDB(BaseDatabase):

  def __init__(self, connection_uri, db_name=CONFIG.database):
    super().__init__(connection_uri)
    self.client = AsyncIOMotorClient(connection_uri)
    self.db = self.client[db_name]
    #self.userinfo = self.client['TELEGRAM']['usercache']
    self.userdata = self.db['userdata']
    self.statial = self.db['statial']

  def __repr__(self):
    return f"tgbot.mongodb(client={self.client})"

  @property
  def name(self):
    return "mongo"

  async def server_info(self):
    return await self.client.server_info()

  async def db_stats(self, database_name):
    db = self.client[database_name]
    return await db.command('dbstats')

  async def list_database(self):
    client = self.client
    database_names = await client.list_database_names()
    return database_names

  async def add_user(self, msg):
    userID = msg.from_user.id
    #userinfo = await self.userinfo.find_one({"userid": userID})
    userdata = await self.userdata.find_one({"userid": userID})
    # if not userinfo:
    #   firstname = msg.from_user.first_name
    #   lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""

    #   uinfo = {
    #       "userid": userID,
    #       "name": [firstname + lastname],
    #       "username": [msg.from_user.username],
    #       "dc": msg.from_user.dc_id if msg.from_user.dc_id else 0,
    #       "firstseen": msg.date,
    #       "lastseen": msg.date
    #   }
    #  await self.userinfo.insert_one(uinfo)

    if not userdata:
      firstname = msg.from_user.first_name
      lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""
      
      data = {
        "userid": userID, 
        "name": [firstname + lastname],
        "username": [msg.from_user.username],
        "dc": msg.from_user.dc_id if msg.from_user.dc_id else 0,
        "firstseen": msg.date, 
        "lastseen": msg.date}
      
      await self.userdata.insert_one(data)
    return True

  async def get_user(self, userID=None, username=None, fetch_info=False):

    key = userID or username

    if key and (key in self.cache):
        return self.cache[key]

    #userdata = None
    #userinfo = None

    if userID:
      userdata = await self.userdata.find_one({"userid": userID})
      #if fetch_info:
        #userinfo = await self.userinfo.find_one({"userid": userID})
    elif username:
      #userinfo = await self.userinfo.find_one({"username": username})
      #if userinfo:
        userdata = await self.userdata.find_one({"username": username})
    else:
      return False

    if userdata:
      data = {}
      data["userid"] = userdata.get("userid")
      data["name"] = userdata['name'][-1] if userdata.get("name") else ""
      data["username"] = userdata['username'][-1] if userdata.get("username") else ""
      data["dc"] = userdata.get("dc", 0)
      data["is_banned"] = bool(userdata.get("is_banned", False))
      data["warns"] = userdata.get("warns", 0)
      data["subscription"] = userdata.get("subscription", {"name": "free"})
      data["status"] = userdata.get("status", "active")
      data["data"] = userdata.get("data", {})
      data["usage"] = userdata.get("usage", {})
      data["settings"] = userdata.get("settings", {})
      data["firstseen"] = userdata.get("firstseen", 0)
      data["lastseen"] = userdata.get("lastseen", 0)
      data["credits"] = userdata.get("credits", 0)
      #if userinfo:

        #data["username"] = userinfo['username'][-1] if userinfo[
        #    'username'] else ""
        #data["dc"] = userinfo['dc']
        #data["name"] = userinfo['name'][-1] if userinfo['name'] else ""
        #data["is_banned"] = bool(userinfo.get("is_banned", False)) or bool(
        #    userdata.get("is_banned", False))
        
      user = utils.gen_user(data)
      self.cache[userID] = user
      return user
    else:
      return None

  async def find_user(self, data, fetch_info=False):
    #if (userID in self.cache) and ((not fetch_info) or (self.cache[userID]["fetch_info"])):
    #  return self.cache[userID]["user"]
    #userinfo = None
    userdata = None

    userdata = await self.userdata.find_one({
          f'data.{key}': value
          for key, value in data.items()
      })
    if userdata:
      data = {}
      data["userid"] = userdata.get("userid")
      data["is_banned"] = bool(userdata.get("is_banned", False))
      data["warns"] = userdata.get("warns", 0)
      data["subscription"] = userdata.get("subscription", {"name": "free"})
      data["status"] = userdata.get("status", "active")
      data["data"] = userdata.get("data", {})
      data["settings"] = userdata.get("settings", {})
      data["firstseen"] = userdata['firstseen']
      data["lastseen"] = userdata['lastseen']


      data["username"] = userdata['username'][-1] if userdata.get("username") else ""
      data["dc"] = userdata.get("dc", 0)
      data["name"] = userdata['name'][-1] if userdata.get("name") else ""

      user = utils.gen_user(data)
     #caching diabled for find_user:
     #
     # u = {"user": user,
     #     "fetch_info":fetch_info}
     # self.cache[userID] = u
      return user
    else:
      return None

  async def fetch_all_users(self):
    userIDs = []
    cursor = self.userdata.find({"status": {"$ne": "inactive"}}, {"_id": 0, 'userid': 1 })

    try:
      async for document in cursor:
        if document.get("userid", None):
         userIDs.append(document["userid"])
    except Exception as e:
      logger.error(f"An error occurred while fetching users: {e}")
    return userIDs

  async def get_stats(self):
    stats = {}

    total_users = await self.userdata.count_documents({})
    active_users = await self.userdata.count_documents(
        {'lastseen': {
            '$gte': datetime.now() - timedelta(days=7)
        }})

    stats['total_users'] = total_users
    stats['active_users'] = active_users

    statial = await self.statial.find_one({}, {"_id": 0})
    if statial:
      for stat in statial:
        stats[stat] = statial[stat]
    return stats

  async def data_exists(self, data):
    query = {f'data.{key}': value for key, value in data.items()}
    result = await self.userdata.find_one(query)
    return bool(result)

  async def inc_stat(self, what, how):
    await self.statial.update_one({}, {"$inc": {what: how}})
    return True

  async def update_user(self, userID, userdata, dmode="$set"):
    filter = {"userid": userID}

    #if userinfo:
    username = userdata.get("username", None)
    if username:
      await self.userdata.update_one(
          filter,
          {
              "$push": {
                  "username": {
                      "$each": [username],
                      "$slice":
                      -1  # Keep only the last 20 elements in the array
                  }
              }
          })
      userdata.pop("username")
    
    name = userdata.get("name", None)
    if name:
        await self.userdata.update_one(
            filter,
            {
                "$push": {
                    "name": {
                        "$each": [name],
                        "$slice":
                        -1  # Keep only the last 20 elements in the array
                    }
                }
            })
        userdata.pop("name")
      #await self.userdata.update_one(filter, {dmode: userinfo})

    if True: 
      to_pop = []
      for key, value in userdata.items():
        if value == "":
          await self.userdata.update_one(filter, {"$unset": {key: ""}})
          to_pop.append(key)
        if key == "data":
          data = {}
          for subkey, subvalue in value.items():
            if subvalue == "":
              await self.userdata.update_one(filter, {"$unset": {f'data.{subkey}': ""}})
            else:
              data[f'data.{subkey}'] = subvalue
          await self.userdata.update_one(filter, {dmode: data})
          to_pop.append(key)

      for key in to_pop:
        userdata.pop(key, None) 

      await self.userdata.update_one(filter, {dmode: userdata})
      if userID in self.cache:
        del self.cache[userID]

  async def update_lastseen(self, userID, lastseen):
     filter = {"userid": userID}
     await self.userdata.update_one(filter, {"$set": {"lastseen": lastseen}})
     #await self.userinfo.update_one(filter, {"$set": {"lastseen": lastseen}})


  async def delete_user(self, userID, clear_info=False):
    #if clear_info:
    #  await self.userinfo.delete_one({"userid": userID})
    await self.userdata.delete_one({"userid": userID})
    if userID in self.cache:
      del self.cache[userID]
    return True
