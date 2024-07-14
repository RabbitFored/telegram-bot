from pyrogram import Client
from bot.core import filters as fltr
import importlib
from bot import strings
from bot.core import utils

@Client.on_callback_query(fltr.on_marker("cf"))
async def change_function(client, query):
  await query.answer()
  data  = query.data[3:]
  m = '.'.join(data.split(".")[:-1])
  f = data.split(".")[-1]
  module = importlib.import_module(f"bot.plugins.{m}")
  
  func = getattr(module, f , None)
  if callable(func):
    await func(client, query.message)
  else:
    raise AttributeError(f"Function '{func}' not found in module '{module}'")

@Client.on_callback_query(fltr.on_marker("ct"))
async def change_text(client, query):
  await query.answer()
  to_get = query.data[3:]

  text = getattr(strings, to_get+'_TEXT')
  btn = getattr(strings, to_get + '_BTN')

  await query.message.edit(text,reply_markup=utils.generate_keyboard(btn))
