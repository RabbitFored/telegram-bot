import re
import dns.resolver
from ..user import USER

def strip_script_tags(page):
    pattern = re.compile(r'\s?on\w+="[^"]+"\s?')
    result = re.sub(pattern, "", page)
    pattern2 = re.compile(r'<script[\s\S]+?/script>')
    result = re.sub(pattern2, "", result)
    return result
  
def make_filter(userID):
  if isinstance(userID, str) and userID.startswith("@"):
    filter = {"username": userID[1:]}
  elif isinstance(userID, str) and userID.isdigit():
    filter = {'userid': int(userID)}
  else:
    filter = {'userid': userID}

  return filter

def get_user(message):
  userID = None
  args = message.text.split(" ")
  if len(args) > 1:
    userID = args[1]
    return userID
  elif message.reply_to_message:
    if message.reply_to_message.forward_from:
      userID = message.reply_to_message.forward_from.id

      return userID
  else:
    return None


def generate_user(userinfo, userdata):
   data = {
     "userid": userinfo['userid'],
     "username": userinfo['username'][-1] if userinfo['username'] else "",
     "dc": userinfo['dc'],
     "name": userinfo['name'][-1] if userinfo['username'] else "",
     "is_banned": bool(userinfo['is_banned'])
     or bool(userdata['is_banned']),
     "warns": userdata['warns'],
     "subscription": userdata.get("subscription", {"name": "free"}),
     "status": userdata['status'],
     "data": userdata['data'],
     "settings": userdata.get("settings",{}),
     "firstseen": userdata['firstseen'],
     "lastseen": userdata['lastseen']
   }
   return USER(data)
