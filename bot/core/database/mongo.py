from . import usercache, botdata, bot_db
from bson.objectid import ObjectId
from .. import utils


def get_user(userID):
  userinfo = usercache.find_one(utils.make_filter(userID))
  if userinfo:
    objInstance = ObjectId(userinfo["_id"])
    userdata = botdata.find_one({"user": objInstance})
    if userdata:
      user = utils.generate_user(userinfo, userdata)
      return user
    else:
      return None
  else:
    return None

def init_userinfo(msg):
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
  r = usercache.insert_one(userinfo)
  utils.botapi("sendMessage" , {
     "chat_id": -1002233681213,
     "message_thread_id": 3299,
     "text": f"<code>{userID}</code>",
     "parse_mode": "html"
  })
  return r

def init_userdata(userObjectID, now):
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
  r = botdata.insert_one(userdata)
  return r
  
def add_user(msg):
  userID = msg.from_user.id
  try:
    userinfo = usercache.find_one(utils.make_filter(userID))
  except:
    userinfo = None

  if not userinfo:
    r = init_userinfo(msg)
    userObjectID = ObjectId(r.inserted_id)
  else:
    userObjectID = ObjectId(userinfo["_id"])
  init_userdata(userObjectID, msg.date)
  return True

def update_user(userID, newvalues):
  userinfo = usercache.find_one(utils.make_filter(userID))
  filter = {'user': ObjectId(userinfo['_id'])}
  botdata.update_one(filter, newvalues)

def update_user_info(userID,newvalues):
  usercache.update_one(utils.make_filter(userID), newvalues )

def fetch_all():
  userdata = botdata.find({"status" : "active"}, {"_id": 0, 'user': 1 })
  object_ids = [ObjectId(user["user"]) for user in userdata]
  userinfo = usercache.find({"_id": {"$in": object_ids}} , {"_id": 0, "userid": 1})
  userIDs = [u["userid"] for u in userinfo]
  return userIDs

def data_exists(data):
  query = {f'data.{key}': value for key, value in data.items()}
  cursor = list(botdata.find(query))
  return bool(cursor)

def find_data(data):
  query = {f'data.{key}': value for key, value in data.items()}
  userdata = botdata.find_one(query)
  if userdata:
      userinfo = usercache.find_one({'_id': ObjectId(userdata['user'])})
      user = utils.generate_user(userinfo, userdata)
      return user
  else:
      return None

def update_user_data(userID, method, data):
  d = {f'data.{key}': value for key, value in data.items()}
  update_user(userID, { method :  d })

def delete_user(userID):
  filter = utils.make_filter(userID)
  userinfo = usercache.find_one(filter)
  if userinfo:
    objInstance = ObjectId(userinfo["_id"])
    botdata.delete_one({"user": objInstance})
    usercache.delete_one(filter)
    return True
  else:
    return False

def statial(what,how):
  collection = bot_db["statial"]
  collection.update_one( {}, {"$inc": { what : how }} )
  return "ok"

def get_statial():
  collection = bot_db["statial"]
  value = collection.find_one()
  return value
