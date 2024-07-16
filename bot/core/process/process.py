import asyncio

class Process:
    def __init__(self, process_id, name):
        self.process_id = process_id
        self.name = name
        self.task = None
        self.data = {}
    
    async def start(self, coro):
        self.task = asyncio.create_task(coro)

    async def stop(self):
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass

    def is_running(self):
        return self.task and not self.task.done()