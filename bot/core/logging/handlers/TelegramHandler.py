from ...utils import botapi, chunkstring
import logging
from ...shared import CONFIG

class TelegramHandler(logging.Handler):
    def __init__(self, chat_id, thread_id=None, chunk=4000, level=logging.NOTSET):
        super().__init__(level)
        self.chat_id = chat_id
        self.thread_id = thread_id
        self.chunk_size = 4000

    def emit(self, record):
        log_entry = self.format(record)
        logs = chunkstring(log_entry, self.chunk_size)
        for log in logs:
            data = {
            "chat_id": self.chat_id,
            "text": f"<code>{log}</code>",
            "parse_mode": "html"
        }
            if self.thread_id:
                data["message_thread_id"] = self.thread_id
            botapi("sendMessage", data)


formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

tg_logger = CONFIG.settings["logging"]["handlers"]["telegram"]

if tg_logger:
    root_logger = logging.getLogger()

    log_chat = tg_logger.get("chat", None)
    if log_chat:
        log_thread = tg_logger.get("thread", None)
        chunk = tg_logger.get("chunk", 4000)
        tlevel = tg_logger.get("level", "INFO")
        tgHandler = TelegramHandler(chat_id=log_chat,thread_id=log_thread, chunk=chunk)
        tgHandler.setFormatter(formatter)
        tgHandler.setLevel(logging._nameToLevel[tlevel.upper()])
    else:
        root_logger.warn("No chat ID for logging")
else:
    tgHandler=None
