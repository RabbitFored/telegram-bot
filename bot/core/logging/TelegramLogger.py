import logging
from .. import utils
from ..shared import CONFIG
from .handlers import TelegramHandler


formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

tg_logger = CONFIG.settings["logging"]["handlers"]["telegram"]
if tg_logger:
    root_logger = logging.getLogger()

    log_chat = tg_logger.get("chat", None)
    if log_chat:
        log_thread = tg_logger.get("thread", None)
        chunk = tg_logger.get("chunk", 4000)
        tgHandler = TelegramHandler(chat_id=log_chat,thread_id=log_thread, chunk=chunk)
        tgHandler.setFormatter(formatter)
        tgHandler.setLevel(logging.INFO)
        root_logger.addHandler(tgHandler)
    else:
        root_logger.warn("No chat ID for logging")
        
