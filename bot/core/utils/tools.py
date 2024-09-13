import time

import requests
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

from ..shared import CONFIG

units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}

def botapi(method, data=None, bot_token=CONFIG.botTOKEN):
  baseURL = f"https://api.telegram.org/bot{bot_token}/"
  url = baseURL + method
  r = requests.post(url,json=data)
  return r.json()

def get_bytes(size):
   number, unit = [string.strip() for string in size.split()]
   return int(float(number)*units[unit])

def progressBar(count_value, total):
  bar_length = 20
  filled_up_Length = int(round(bar_length* count_value / float(total)))
  percentage = round(100.0 * count_value/float(total),1)
  bar = '█' * filled_up_Length + '▒' * (bar_length - filled_up_Length)
  return bar, percentage



PRGRS = {}

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
          ((str(hours) + "h, ") if hours else "") + \
          ((str(minutes) + "m, ") if minutes else "") + \
          ((str(seconds) + "s, ") if seconds else "") + \
          ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def progress_func(
    current,
    total,
    ud_type,
    message,
    start
):
  now = time.time()
  diff = now - start
  if round(diff % 5.00) == 0 or current == total:
    percentage = current * 100 / total
    speed = current / diff
    af = total / speed
    elapsed_time = round(af) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion
    eta =  TimeFormatter(milliseconds=time_to_completion)
    elapsed_time = TimeFormatter(milliseconds=elapsed_time)
    estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

    PRGRS[f"{message.chat.id}_{message.id}"] = {
        "current": humanbytes(current),
        "total": humanbytes(total),
        "speed": humanbytes(speed),
        "progress": percentage,
        "eta": eta
    }


async def check_sub(client,chatID, userID, ignore_error=False):
  from bot import logger
  try:
    await client.get_chat_member(chatID, userID)
    return True
  except UserNotParticipant:
    return False
  except Exception as e:
    logger.error(f"Error while check chat member: {e}")
    return ignore_error
