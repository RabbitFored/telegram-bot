from datetime import datetime, timedelta, timezone
from os import pread, uname
from ..database import db
from ..shared import CONFIG
import requests
from ..utils import parse_period


class Data(dict):

   def __init__(self, userID, *args):
      super().__init__(*args)
      self.userID = userID

   async def addToSet(self, value):
      await db.update_user(userID=self.userID,
                           userdata={"data": value},
                           dmode="$addToSet")

   async def set(self, value):
      await db.update_user(userID=self.userID, userdata={"data": value})

   async def rm(self, value):
      await db.update_user(userID=self.userID,
                           userdata={"data": value},
                           dmode="$pull")


class Credits:

   def __init__(self, userID, value):
      self.userID = userID
      self.value = value

   async def consume(self, amt=1):
      await db.update_user(userID=self.userID,
                           userinfo={"credits": -amt},
                           dmode="$inc")
      self.value -= amt

   async def provide(self, amt=1):
      await db.update_user(userID=self.userID,
                           userinfo={"credits": amt},
                           dmode="$inc")
      self.value += amt


class Usage(dict):

   def __init__(self, userID, usage):
      self.userID = userID
      self.usage = usage

   async def refresh(self):
      for name in self.usage:
         expiry = self.usage[name].get("expiry", None)
         refresh_period = self.usage[name].get("refresh_period", None)
         round_to_start = self.usage[name].get("round_to_start", False)
         if expiry is not None and expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)

         if expiry and expiry < datetime.now(timezone.utc):
            if refresh_period:
               data = {}
               reset_time = self.calculate_reset_time(refresh_period,
                                                      round_to_start)
               data[f"usage.{name}.value"] = 0
               data[f"usage.{name}.refresh_period"] = refresh_period
               data[f"usage.{name}.expiry"] = reset_time
               await db.update_user(userID=self.userID, userdata=data)
            else:
               await self.unset(name)

   def calculate_reset_time(self, refresh_period: str, round_to_start=False):
      now = datetime.now(timezone.utc)
      unit = refresh_period[-1]

      if round_to_start:
         if unit == 'd':
            return now.replace(hour=0, minute=0, second=0,
                               microsecond=0) + timedelta(days=1)
         elif unit == 'm':
            next_month = (now.month % 12) + 1
            next_year = now.year + (now.month // 12)
            return now.replace(year=next_year,
                               month=next_month,
                               day=1,
                               hour=0,
                               minute=0,
                               second=0,
                               microsecond=0)
         elif unit == 'y':
            return now.replace(year=now.year + 1,
                               month=1,
                               day=1,
                               hour=0,
                               minute=0,
                               second=0,
                               microsecond=0)
         else:
            pass

      return now + parse_period(refresh_period)

   async def set(self,
                 name,
                 value=None,
                 refresh_period=None,
                 expiry=None,
                 round_to_start=False):
      await self.refresh()
      data = {}
      if value:
         data[f"usage.{name}.value"] = value
      if refresh_period:
         data[f"usage.{name}.refresh_period"] = refresh_period
         if not expiry:
            reset_time = self.calculate_reset_time(refresh_period,
                                                   round_to_start)
            data[f"usage.{name}.expiry"] = reset_time
      if expiry:
         data[f"usage.{name}.expiry"] = expiry
      if round_to_start:
         data[f"usage.{name}.round_to_start"] = round_to_start

      await db.update_user(userID=self.userID, userdata=data)

   async def inc(self,
                 name,
                 value=1,
                 refresh_period=None,
                 expiry=None,
                 round_to_start=False):
      await self.refresh()
      if name not in self.usage:
         await self.set(name,
                        value=value,
                        refresh_period=refresh_period,
                        expiry=expiry,
                        round_to_start=round_to_start)
      else:
         if refresh_period and refresh_period != self.usage[name][
             "refresh_period"]:
            await self.set(name,
               value=self.usage[name].get("value", 0) + value,
               refresh_period=refresh_period,
               expiry=expiry,
               round_to_start=round_to_start)
         else:
           await db.update_user(userID=self.userID,
              userdata={f"usage.{name}.value": value},
              dmode="$inc")
   async def unset(self, name):
      await db.update_user(userID=self.userID,
                           userdata={f"usage.{name}": ""},
                           dmode="$unset")

   def get(self, name, default=0):
      if name in self.usage:
         return self.usage[name]["value"]
      else:
         return default


class USER:

   def __init__(self, data):
      self.ID = data.get('userid', None)
      self.name = data.get('name', None)
      self.username = data.get('username', None)
      self.dc = data.get('dc', None)
      self.status = data.get('status', None)
      self.is_banned = data.get('is_banned', None)
      self.warns = data.get('warns', None)
      self.credits = Credits(self.ID, data.get('credits', 0))
      self.data = Data(self.ID, data.get('data', {}))
      self.usage = Usage(self.ID, data.get('usage', {}))
      self.settings = data.get('settings', {})
      self.subscription = data.get('subscription', {})
      self.firstseen = data.get('firstseen', None)
      self.lastseen = data.get('lastseen', None)

   def get_limits(self):
      subscriptions = CONFIG.settings["subscriptions"]
      for subscription in subscriptions:
         if subscription["name"] == self.subscription['name']:
            return subscription["data"]["limits"]

   async def upgrade(self, plan, transaction_id):
      userdata = {
          "subscription.name":
          plan,
          "subscription.subscription_date":
          datetime.now(timezone.utc),
          "subscription.expiry_date":
          datetime.now(timezone.utc) + timedelta(days=30),
          "subscription.transaction_id":
          transaction_id,
      }
      await db.update_user(self.ID, userdata=userdata)

   async def gift(self, plan, byUSER):
      userdata = {
          "subscription.name":
          plan,
          "subscription.subscription_date":
          datetime.now(timezone.utc),
          "subscription.expiry_date":
          datetime.now(timezone.utc) + timedelta(days=30),
          "subscription.gift_by":
          byUSER
      }
      await db.update_user(self.ID, userdata=userdata)

   async def end_subscription(self, userID):
      userdata = {"subscription": ""}
      await db.update_user(userID, userdata=userdata)
      data = {
          "chat_id": self.ID,
          "text":
          "<b>Your subscription expired.\n\nUse /upgrade to continue enjoying premium features</b>",
          "parse_mode": "html"
      }

      requests.post(
          f"https://api.telegram.org/bot{CONFIG.botTOKEN}/sendMessage",
          json=data)

   async def refresh(self, msg):
      userinfo = {}
      userdata = {}

      #update lasteen
      now = msg.date
      await db.update_lastseen(self.ID, now)

      #make user active
      if self.status == "inactive":
         userdata["status"] = "active"

      #set dc
      if self.dc == 0 and msg.from_user.dc_id:
         userinfo["dc"] = msg.from_user.dc_id

      if msg.from_user.username != self.username:
         userinfo["username"] = msg.from_user.username

      firstname = msg.from_user.first_name
      lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""

      name = firstname + lastname
      if self.name != name:
         userinfo["name"] = name
      await db.update_user(self.ID, userinfo, userdata)
      if self.subscription and self.subscription["name"] != "free":
         if now > self.subscription['expiry_date']:
            await self.end_subscription(self.ID)
      await self.usage.refresh()

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
