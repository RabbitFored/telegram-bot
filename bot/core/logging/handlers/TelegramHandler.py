from ...utils import botapi, chunkstring
import logging

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
