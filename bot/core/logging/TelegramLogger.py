import logging
from .. import utils
from ..shared import CONFIG


class TelegramHandler(logging.Handler):

    def __init__(self, chat_id, level=logging.NOTSET):
        super().__init__(level)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        utils.botapi(
            "sendMessage", {
                "chat_id": self.chat_id,
                "text": f"<code>{log_entry}</code>",
                "message_thread_id": 2,
                "parse_mode": "html"
            })


LOG_CHANNEL = CONFIG.settings.get("LOG_CHANNEL", None)
if LOG_CHANNEL:
    tgHandler = TelegramHandler(chat_id=LOG_CHANNEL)
    tgHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    tgHandler.setFormatter(formatter)
else:
    tgHandler = None
