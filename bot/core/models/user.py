from datetime import datetime, timedelta
from os import pread, uname
from ...core import database as db
from ..shared import CONFIG
import requests
import time

class Data(dict):

   def __init__(self, userID, *args):
      super().__init__(*args)
      self.userID = userID

   async def addToSet(self, value):
      await db.update_user_data(self.userID, "$addToSet", value)

   async def set(self, value):
      await db.update_user_data(self.userID, "$set", value)

   async def rm(self, value):
      await db.update_user_data(self.userID, "$pull", value)


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

   async def add_data(self, data):
      await db.update_user_data(self.ID, "$addToSet", data)

   async def set_data(self, data):
      await db.update_user_data(self.ID, "$set", data)

   async def rm_data(self, data):
      await db.update_user_data(self.ID, "$pull", data)

   async def upgrade(self, plan, transaction_id):
      await db.update_user(
          self.ID, {
              "$set": {
                  "subscription.name": plan,
                  "subscription.subscription_date": datetime.now(),
                  "subscription.expiry_date":
                  datetime.now() + timedelta(days=30),
                  "subscription.transaction_id": transaction_id,
              }
          })
   async def gift(self,plan, byUSER):
      await db.update_user(
          self.ID, {
              "$set": {
                  "subscription.name": plan,
                  "subscription.subscription_date": datetime.now(),
                  "subscription.expiry_date":
                  datetime.now() + timedelta(days=30),
                  #"subscription.transaction_id": transaction_id,
                 "subscription.gift_by" : byUSER
              }
          })
   async def remove_subscription(self, userID):
      await db.update_user(userID, {"$unset": {"subscription": ""}})

   async def refresh(self, msg):
      
      #update lasteen
      lastseen = msg.date
      await db.update_lastseen(self.ID, lastseen)
      
      #await db.update_user(msg.from_user.id, {"$set": newValues})
      #await db.update_user_info(msg.from_user.id, {"$set": newValues})

      #make user active
      if self.status == "inactive":
         await db.update_user(self.ID, {"$unset": {"status": ""}})

      #set dc
      if self.dc == 0 and msg.from_user.dc_id:
         db.update_user_info(msg.from_user.id,
                             {"$set": {
                                 "dc": msg.from_user.dc_id
                             }})

      #update user info
      if msg.from_user.username != self.username:
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
      if self.name != name:
         await db.update_user_info(
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
               await self.remove_subscription(self.ID)
               data = {
                  "chat_id": self.ID,
                  "text": "<b>Your subscription expired.\n\nUse /upgrade to continue enjoying premium features</b>",
                  "parse_mode": "html"
                  }
               
               r = requests.post(f"https://api.telegram.org/bot{CONFIG.botTOKEN}/sendMessage", 
                                 json=data)
      

   async def ban(self):
      await db.update_user(self.ID, {"$set": {"is_banned": True}})

   async def unban(self):
      await db.update_user(self.ID, {"$unset": {"is_banned": ""}})

   async def clear_warns(self):
      await db.update_user(self.ID, {"$unset": {"warns": ""}})

   async def warn(self):
      max_warn = 3
      if self.warns > max_warn:
         await self.ban()
         return
      else:
         await db.update_user(self.ID, {"$inc": {"warns": 1}})

   async def setStatus(self, status):
      await db.update_user(self.ID, {"$set": {"status": status}})
