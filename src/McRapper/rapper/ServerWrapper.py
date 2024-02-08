import asyncio
from .events import *
import os
import logging


class Context:
    def __init__(self, time=None, thread=None, level=None, event=None, content=None):
        self.time = time
        self.thread = thread
        self.level = level
        self.event = event
        self.content = content


class ServerWrapper:
    def __init__(self, server_path, env=None):
        self.env = env
        if not self.env:
            self.env = os.environ.get('PWD')

        self.server_path = server_path
        self.events = EventHandler()
        self._process = None

    async def create_process(self) -> asyncio.subprocess.Process:
        process = await asyncio.create_subprocess_exec(
                'java', '-jar', self.server_path, "nogui",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                #cwd=f"{self.env}"
        )
        return process

    def start(self):

        async def sub_start():
            self._process = await self.create_process()
            x = await self._monitor()
        try:
            asyncio.run(sub_start())

        except KeyboardInterrupt:
            print('Received KeyBoardInterrupt')
            self._process.terminate()
        except Exception as e:
            logging.error(e)

    async def _monitor(self):
        while True:
            line = await self._process.stdout.readline()
            ctx = self._check_line(line.decode())
            logging.info(line.decode())
            logging.info(f"{ctx.time} {ctx.thread}/{ctx.level}\n\tEvent: {ctx.event}: {ctx.content} ")
            if ctx.event:
                await self.events.run_hooks(ctx)

    async def _send_cmd(self, cmd):
        out, err = await self._process.communicate(f"{cmd}\n".encode())
        print(out)
        print(err)

    @staticmethod
    def _check_line(line) -> Context:
        ctx = Context()

        for lev in Levels:
            log_match = lev.value.match(line)
            if log_match:
                match lev:
                    case Levels.SYSTEM:
                        ctx.level = Levels.SYSTEM
                        ctx.content = log_match.group(0)
                        events = SystemEvents
                    case Levels.ERROR:
                        ctx.level = Levels.ERROR
                        ctx.content = log_match.group(0)
                        events = ErrorEvents
                    case Levels.INFO:
                        ctx.level = lev
                        ctx.time = log_match.group(1)
                        ctx.thread = log_match.group(2)
                        ctx.content = log_match.group(3)
                        events = InfoEvents
                    case Levels.WARN:
                        ctx.level = lev
                        ctx.time = log_match.group(1)
                        ctx.thread = log_match.group(2)
                        ctx.content = log_match.group(3)
                        events = WarnEvents
                    case _:
                        events = []
                for e in events:
                    if e.value.match(ctx.content):
                        ctx.event = e
        return ctx


if __name__ == "__main__":
    m = ServerWrapper("/Users/novapy/Downloads/mcrapper/serverv/minecraft_server.1.20.4.jar")

    @m.events.on(SystemEvents.EXEC_START)
    async def start(ctx):
        print(f"{ctx.time} SERVER HAS STARTED")
        return True
    m.start()

