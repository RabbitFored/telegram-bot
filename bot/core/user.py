from datetime import datetime, timedelta
from ..core import database as db
from .shared import CONFIG

class Data(dict):
   def __init__(self, userID, *args):
        super().__init__(*args)
        self.userID = userID

   def addToSet(self, value):
       db.update_user_data(self.userID, "$addToSet", value)
   def set(self, value):
       db.update_user_data(self.ID, "$set", value)
   def rm(self, value):
       db.update_user_data(self.ID, "$pull", value)

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

   def upgrade(self, userID, plan, transaction_id):
      db.update_user(
         userID, {
            "$set": {
               "subscription.name": plan,
               "subscription.subscription_date": datetime.now(),
               "subscription.expiry_date": datetime.now() + timedelta(days=30),
               "subscription.transaction_id": transaction_id,
            }
         })

   def remove_subscription(self, userID):
      db.update_user(userID, {"$set": {"subscription": {"name": "free"}}})

   def refresh(self, msg):

      newValues = {'lastseen': msg.date}

      db.update_user(msg.from_user.id, {"$set": newValues})
      #db.user.update_info( msg.from_user.id ,  { "$set": newValues } )

      if self.subscription:
         if not self.subscription["name"] == "free":
            if datetime.now() > self.subscription['expiry_date']:
               self.remove_subscription(self.ID)

   def ban(self):
      db.update_user(self.ID, {"$set": {"is_banned": True}})
      
   def unban(self):
      db.update_user(self.ID, {"$set": {"is_banned": False}})