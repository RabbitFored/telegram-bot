from datetime import datetime, timedelta
from os import pread
from ...core import database as db
from ..shared import CONFIG
import requests

class Data(dict):

   def __init__(self, userID, *args):
      super().__init__(*args)
      self.userID = userID

   def addToSet(self, value):
      db.update_user_data(self.userID, "$addToSet", value)

   def set(self, value):
      db.update_user_data(self.userID, "$set", value)

   def rm(self, value):
      db.update_user_data(self.userID, "$pull", value)


class USER:

   def __init__(self, data):
      self.ID = data['userid']
      self.name = data['name']
      self.username = data['username']
      self.dc = data['dc']
      self.status = data['status']
      self.is_banned = data['is_banned']
      self.warns = data['warns']
      self.data = Data(self.ID, data.get('data', {}))
      self.settings = data['settings']
      self.subscription = data['subscription']
      self.firstseen = data['firstseen']
      self.lastseen = data['lastseen']

   def get_limits(self):
      subscriptions = CONFIG.settings["subscriptions"]
      for subscription in subscriptions:
         if subscription["name"] == self.subscription['name']:
            return subscription["data"]["limits"]

   def add_data(self, data):
      db.update_user_data(self.ID, "$addToSet", data)

   def set_data(self, data):
      db.update_user_data(self.ID, "$set", data)

   def rm_data(self, data):
      db.update_user_data(self.ID, "$pull", data)

   def upgrade(self, plan, transaction_id):
      db.update_user(
          self.ID, {
              "$set": {
                  "subscription.name": plan,
                  "subscription.subscription_date": datetime.now(),
                  "subscription.expiry_date":
                  datetime.now() + timedelta(days=30),
                  "subscription.transaction_id": transaction_id,
              }
          })

   def remove_subscription(self, userID):
      db.update_user(userID, {"$set": {"subscription": {}}})

   def refresh(self, msg):
      pre_user = db.get_user(msg.from_user.id)

      now = msg.date
      #update lasteen
      newValues = {'lastseen': msg.date}
      db.update_user(msg.from_user.id, {"$set": newValues})
      db.update_user_info(msg.from_user.id, {"$set": newValues})

      #make user active
      if pre_user.status == "inactive":
         db.update_user(self.ID, {"$unset": {"status": ""}})

      #set dc
      if pre_user.dc == 0 and msg.from_user.dc_id:
         db.update_user_info(msg.from_user.id,
                             {"$set": {
                                 "dc": msg.from_user.dc_id
                             }})

      #update user info
      if msg.from_user.username != pre_user.username:
         db.update_user_info(
             msg.from_user.id,
             {
                 "$push": {
                     "username": {
                         "$each": [msg.from_user.username],
                         "$slice":
                         -20  # Keep only the last 20 elements in the array
                     }
                 }
             })
      firstname = msg.from_user.first_name
      lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""

      name = firstname + lastname
      if pre_user.name != name:
         db.update_user_info(
             msg.from_user.id,
             {
                 "$push": {
                     "name": {
                         "$each": [name],
                         "$slice":
                         -20  # Keep only the last 20 elements in the array
                     }
                 }
             })

      if self.subscription:
         if not self.subscription["name"] == "free":
            if now > self.subscription['expiry_date']:
               self.remove_subscription(self.ID)
               data = {
                  "chat_id": self.ID,
                  "text": "<b>Your subscription expired.\n\nUse /upgrade to continue enjoying premium features</b>",
                  "parse_mode": "html"
                  }
               
               r = requests.post(f"https://api.telegram.org/bot{CONFIG.botTOKEN}/sendMessage", 
                                 json=data)
      

   def ban(self):
      db.update_user(self.ID, {"$set": {"is_banned": True}})

   def unban(self):
      db.update_user(self.ID, {"$set": {"is_banned": False}})

   def clear_warns(self):
      db.update_user(self.ID, {"$unset": {"warns": ""}})
   def warn(self):
      max_warn = 3
      if self.warns > max_warn:
         self.ban()
         return
      else:
        db.update_user(self.ID, {"$inc": {"warns": 1}})

   def setStatus(self, status):
      db.update_user(self.ID, {"$set": {"status": status}})
