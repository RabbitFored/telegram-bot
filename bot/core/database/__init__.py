import glob
import importlib
from os.path import basename, dirname, isfile

from .mongo_mono import MongoDB
#from .redis import Redis
from ..shared import CONFIG

db = MongoDB(CONFIG.mongouri)

#db = Redis("test")
#def list_all_modules():
    # This generates a list of modules in this folder
#    mod_paths = glob.glob(dirname(__file__) + "/*.py")
#    all_modules = [
#       basename(f)[:-3] for f in mod_paths if isfile(f) and f.endswith(".py")
#        and not f.endswith("__init__.py") and not f.endswith("__main__.py")
#    ]
#
#    return all_modules


#ALL_MODULES = ["mongo"]

#for i in ALL_MODULES:
#    mdl = importlib.import_module(f'bot.core.database.{i}')
#    names = [x for x in mdl.__dict__ if not x.startswith("_")]
#    globals().update({k: getattr(mdl, k) for k in names})

#    globals().update({k: getattr(mdl, k) for k in names})
