from pyrogram import Client
from bot.core import filters as fltr
import importlib
from bot import strings, ProcessManager 
from bot.core import utils
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(fltr.on_marker("cf"))
async def change_function(client, query):
  await query.answer()
  data  = query.data[3:]
  m = '.'.join(data.split(".")[:-1])
  f = data.split(".")[-1]
  module = importlib.import_module(f"bot.plugins.{m}")
  
  func = getattr(module, f , None)
  if callable(func):
    await func(client, query.message.reply_to_message)
  else:
    raise AttributeError(f"Function '{func}' not found in module '{module}'")

@Client.on_callback_query(fltr.on_marker("ct"))
async def change_text(client, query):
  await query.answer()
  to_get = query.data[3:]
  text = strings.get(to_get  + '_txt')
  await query.message.edit(text)

@Client.on_callback_query(fltr.on_marker("ps"))
async def ps(client, query):
    process = ProcessManager.list_processes()
    for p in process:
      if p.name == 'broadcast':
        keyboard = [
          [
              InlineKeyboardButton("Check Progress", callback_data="ps_broadcast"),
          ]
        ]
        success = p.data['x']
        failed = p.data['failed']
        
        count, total = success + failed, p.data["total"]
        bar, percentage = utils.progressBar(count, total)

        text = f'''
<b>BROADCASTING {count} of {total}</b>
success: {success}
failed: {failed}

| {bar} | {percentage}%
        '''

        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard),parse_mode=enums.ParseMode.HTML)