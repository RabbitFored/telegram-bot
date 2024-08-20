'''
from datetime import datetime, timedelta

import aioredis

from .. import utils
from ..shared import CONFIG
from .base import BaseDatabase


class Redis(BaseDatabase):

  def __init__(self, connection_uri):
    super().__init__(connection_uri)
    self.client = aioredis.from_url("redis://redis-11796.c81.us-east-1-2.ec2.redns.redis-cloud.com:11796", password='')

  def __repr__(self):
    return f"tgbot.redis(client={self.client})"
    
  @property
  def name(self):
    return "redis"

  async def add_user(self, msg):
     userID = msg.from_user.id


     firstname = msg.from_user.first_name
     lastname = " " + msg.from_user.last_name if msg.from_user.last_name else ""
    
     udata = {
       "name": [firstname + lastname],
       "username": [msg.from_user.username],
       "dc": msg.from_user.dc_id if msg.from_user.dc_id else 0,
       "firstseen": msg.date,
       "lastseen": msg.date
     }
     await self.client.hset(f"{userID}", mapping=udata)
     return True
  async def get_user(self, userID, fetch_info=False):
    return False
'''
#TODO