from datetime import datetime, timedelta
from os import pread, uname
from ..database import db
from ..shared import CONFIG
import requests
import time

class Data(dict):

   def __init__(self, userID, *args):
      super().__init__(*args)
      self.userID = userID

   async def addToSet(self, value):
      await db.update_user(userID=self.userID, userdata={"data" : value},dmode="$addToSet")

   async def set(self, value):
      await db.update_user(userID=self.userID, userdata={"data" : value})

   async def rm(self, value):
      await db.update_user(userID=self.userID, userdata={"data" : value}, dmode="$pull")


class USER:
   def __init__(self, data):
      self.ID = data.get('userid', None)
      self.name =  data.get('name', None)
      self.username =  data.get('username', None)
      self.dc = data.get('dc', None)
      self.status =  data.get('status', None)
      self.is_banned =  data.get('is_banned', None)
      self.warns =  data.get('warns', None)
      self.data = Data(self.ID, data.get('data', {}))
      self.settings =  data.get('settings', {})
      self.subscription =  data.get('subscription', {})
      self.firstseen =  data.get('firstseen', None)
      self.lastseen =  data.get('lastseen', None)

   def get_limits(self):
      subscriptions = CONFIG.settings["subscriptions"]
      for subscription in subscriptions:
         if subscription["name"] == self.subscription['name']:
            return subscription["data"]["limits"]

   async def upgrade(self, plan, transaction_id):
      userdata = {
            "subscription.name": plan,
            "subscription.subscription_date": datetime.now(),
            "subscription.expiry_date":
            datetime.now() + timedelta(days=30),
            "subscription.transaction_id": transaction_id,
        }
      await db.update_user(self.ID, userdata=userdata)

   async def gift(self,plan, byUSER):
      userdata = {
         "subscription.name": plan,
         "subscription.subscription_date": datetime.now(),
         "subscription.expiry_date":
         datetime.now() + timedelta(days=30),
         "subscription.gift_by" : byUSER
      }
      await db.update_user(self.ID, userdata=userdata)
      
   async def remove_subscription(self, userID):
      userdata = {"subscription": ""}
      await db.update_user(userID, userdata=userdata)

   async def refresh(self, msg):
      userinfo = {}
      userdata = {}
      
      #update lasteen
      lastseen = msg.date
      
      userinfo["lastseen"] = lastseen
      userdata["lastseen"] = lastseen

      #make user active
      if self.status == "inactive":
         userdata["status"] = "active"

      #set dc
      if self.dc == 0 and msg.from_user.dc_id:
        userinfo["dc"] =  msg.from_user.dc_id

      if msg.from_user.username != self.username:
         userinfo["username"] = msg.from_user.username

      firstname = msg.from_user.first_name
      lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""

      name = firstname + lastname
      if self.name != name:
         userinfo["name"] = name
      await db.update_user(self.ID, userinfo, userdata)
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
      userdata = {"is_banned": True}
      await db.update_user(self.ID, userdata=userdata)

   async def unban(self):
      userdata = {"is_banned": ""}
      await db.update_user(self.ID, userdata=userdata)

   async def clear_warns(self):
      userdata = {"warns": ""}
      await db.update_user(self.ID, userdata=userdata)

   async def warn(self):
      max_warn = 3
      if self.warns > max_warn:
         await self.ban()
         return
      else:
         userdata = {"warns": self.warns + 1}
         await db.update_user(self.ID, userdata=userdata)

   async def setStatus(self, status):
      userdata = {"status": status}
      await db.update_user(self.ID, userdata=userdata)
