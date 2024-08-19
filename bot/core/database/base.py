from cachetools import TTLCache


class BaseDatabase:
  def __init__(self, uri=None):
    self.uri = uri
    self.cache = TTLCache(maxsize=1000, ttl=60)

  def clear_cache(self):
    self.cache.clear()
    return True
    