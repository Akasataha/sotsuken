import asyncio


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def start(self, name, coro):
        if name in self.tasks:
            print(f"{name}は既に存在しています")
            return
        self.tasks[name] = asyncio.create_task(coro)

    async def stop(self, name):
        task: asyncio.Task = self.tasks.pop(name, None)
        if task:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    async def stop_all(self):
        for task in self.tasks.values():
            task.cancel()
        for task in self.tasks.values():
            try:
                await task
            except asyncio.CancelledError:
                pass
        self.tasks.clear()
