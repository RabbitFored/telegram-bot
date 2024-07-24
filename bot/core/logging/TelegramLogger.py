import logging
from .. import utils
from ..shared import CONFIG


class TelegramHandler(logging.Handler):

    def __init__(self, chat_id, thread_id=None, level=logging.NOTSET):
        super().__init__(level)
        self.chat_id = chat_id
        self.thread_id = thread_id
        
    def emit(self, record):
        log_entry = self.format(record)
        logs = utils.chunkstring(log_entry, 4000)
        for log in logs:
            data = {
                "chat_id": self.chat_id,
                "text": f"<code>{log}</code>",
                "parse_mode": "html"
            }
            if self.thread_id:
                data["message_thread_id"] = self.thread_id
            utils.botapi("sendMessage", data)
            


LOG_CHANNEL = CONFIG.settings.get("LOG_CHANNEL", None)
LOG_THREAD = CONFIG.settings.get("LOG_THREAD", None)
if LOG_CHANNEL:
    tgHandler = TelegramHandler(chat_id=LOG_CHANNEL,thread_id=LOG_THREAD)
    tgHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    tgHandler.setFormatter(formatter)
else:
    tgHandler = None
