import time
from .shared import CONFIG
from collections import defaultdict, deque


class AntiFlood:
    def __init__(self, max_messages, time_window):
        self.max_messages = max_messages
        self.time_window = time_window
        self.user_messages = defaultdict(deque)

    def is_flooding(self, user_id):
        current_time = time.time()
        message_times = self.user_messages[user_id]

        # Remove messages outside the time window
        while message_times and message_times[0] < current_time - self.time_window:
            message_times.popleft()

        # Check if user is flooding
        if len(message_times) >= self.max_messages:
            return True

        # Record the new message time
        message_times.append(current_time)
        print(message_times)
        return False
    def flush_user(self, user_id):
        """ Clears stored message times for a specific user. """
        if user_id in self.user_messages:
            del self.user_messages[user_id]

if CONFIG.settings["user_check"].get("antiflood", None):
  message_interval = CONFIG.settings["user_check"]["antiflood"].get("message_interval",5)
  message_count = CONFIG.settings["user_check"]["antiflood"].get("message_count",5)
  antiflood = AntiFlood(message_count, message_interval)
else:
    antiflood = None