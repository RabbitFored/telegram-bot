import regex as re
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def ikb(markdown):
  pattern = re.compile(r'\[([^][]+)\](\(((?:[^()]+|(?2))+)\))')
  
  rows = list(filter(None, markdown.split("\n") ))
  keyboard = []
  
  for row in rows:
    buttons = []
    for match in pattern.finditer(row):
      text, _, data = match.groups()  
      type = data.split("::")[0]
      value = data[len(type) + 2:]

      if type == "url":
        buttons.append(InlineKeyboardButton(text, url=value))
      elif type == "data":
        buttons.append(InlineKeyboardButton(text, callback_data=value))
      else:
        print("Unknown keyboard type: ", type)
    
    keyboard.append(buttons)
  
  return InlineKeyboardMarkup(keyboard)

generate_keyboard = ikb