import importlib
from .logging import logger
from . import user, database
from .process import ProcessManager

ALL_MODULES = ["user"]

for i in ALL_MODULES:
  mdl = importlib.import_module(f'bot.core.{i}')
  names = [x for x in mdl.__dict__ if not x.startswith("_")]
  globals().update({k: getattr(mdl, k) for k in names})
