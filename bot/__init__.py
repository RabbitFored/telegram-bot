from .core import logger
import sys
from .core import ProcessManager
from .core.shared import CONFIG
from .core import Translator
import os
import tempfile
from .core.internals import bot, web
import subprocess
import shutil

#if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logger.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

# setting up processes
ProcessManager = ProcessManager()

# Initialize strings
default_language = CONFIG.settings["translation"]["default_language"]
lang_dir = CONFIG.settings["translation"]["dir"]

strings = Translator(dir=lang_dir, default_language=default_language)


#make temp dir
try:
    os.makedirs("/tmp/bot", exist_ok=True)
    tempfile.tempdir = "/tmp/bot"
    print("Directory created successfully")
except OSError as error:
    print(f"Directory can not be created, {error}")

#install plugins

with tempfile.TemporaryDirectory(prefix=f"plugins_") as temp_dir:
    plugins = CONFIG.settings.get("plugins", None)

    if plugins:
        PLUGIN_DIR = CONFIG.settings["plugins"].get("dir", "bot/plugins")
        DOWNLOAD_DIR = temp_dir
        REPO_URL = plugins.get("repo", [])
        PLUGIN_LIST = plugins.get("include", [])

        for REPO in REPO_URL:
          try:
              subprocess.run(['git', 'clone', REPO, DOWNLOAD_DIR], check=True)
          except Exception:
              logger.error(f"Caught error while cloning {REPO}")

        for plugin in PLUGIN_LIST:
            source = os.path.join(DOWNLOAD_DIR, plugin)
            destination = os.path.join(PLUGIN_DIR, plugin)
            if os.path.exists(source):
                  shutil.copytree(source, destination, dirs_exist_ok=True)
            else:
                  logger.info(f"Plugin {plugin} not found")