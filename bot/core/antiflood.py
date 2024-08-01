import time
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
        return False

# Singleton pattern for easy access
antiflood = AntiFlood(5, 5)