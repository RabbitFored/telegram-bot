from ..shared import CONFIG
import requests

def botapi(method, data, bot_token=CONFIG.botTOKEN):
  baseURL = f"https://api.telegram.org/bot{bot_token}/"
  url = baseURL + method
  r = requests.post(url,json=data)
  return r.json()


def get_mx_server(domain):
   try:
        mail_servers = dns.resolver.resolve(domain, 'MX')
        mail_servers = list(set([data.exchange.to_text()[:-1] if data.exchange.to_text().endswith('.') else data.exchange.to_text() for data in mail_servers]))
        return mail_servers
   except:
        return([], [])