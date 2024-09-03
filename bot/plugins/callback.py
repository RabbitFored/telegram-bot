from pyrogram import Client
from bot.core import filters as fltr
import importlib
from bot import strings, ProcessManager , logger
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
    pid = query.data.split("_")[-1]
    process = ProcessManager.get_process(int(pid))
    if process:
        keyboard = [
      [
          InlineKeyboardButton("Check Progress", callback_data=f"ps_{process.process_id}"),
      ]
  ]
        success = process.data['x']
        failed = process.data['failed']
        
        count, total = success + failed, process.data["total"]
        bar, percentage = utils.progressBar(count, total)

        text = f'''
<b>BROADCASTING {count} of {total}</b>
success: {success}
failed: {failed}

| {bar} | {percentage}%
        '''
        try:
          await query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=enums.ParseMode.HTML)
        except Exception as e:
          logger.error(e)
        await query.answer(f"Broadcasting {count} of {total}")
    else:
        await query.answer("No broadcast process is running")