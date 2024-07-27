from ..shared import CONFIG
import requests

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

'''
def get_mx_server(domain):
   try:
        mail_servers = dns.resolver.resolve(domain, 'MX')
        mail_servers = list(set([data.exchange.to_text()[:-1] if data.exchange.to_text().endswith('.') else data.exchange.to_text() for data in mail_servers]))
        return mail_servers
   except:
        return([], [])
'''