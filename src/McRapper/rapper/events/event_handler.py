from re import compile
from enum import Enum


class Levels(Enum):
    INFO = compile(r"\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\s\[(.*)/INFO]:\s(.*)")
    WARN = compile(r"\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\s\[(.*)/WARN]:\s(.*)")
    ERROR = compile(r"\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\s\[(.*)/ERROR]:\s(.*)")
    SYSTEM = compile(r"([a-zA-Z.]*)")


class InfoEvents(Enum):
    ENVIRONMENT = compile(
        r"Environment:\s.*sessionHost=(?P<sessionHost>.*),\sservicesHost=(?P<serviceHost>.*),\sname=(?P<name>.*)]"
    )


class WarnEvents(Enum):
    pass


class ErrorEvents(Enum):
    pass


class SystemEvents(Enum):
    EXEC_START = compile(r"Starting\s.+")


class Events(Enum):
    INFO: Enum = InfoEvents
    WARN: Enum = WarnEvents
    ERROR: Enum = ErrorEvents
    SYSTEM: Enum = SystemEvents


class EventHandler:
    def __init__(self):
        self.hooks = {}
        for events in Events:
            self.hooks.update({event: [] for event in events.value})

    async def run_hooks(self, ctx):
        if ctx.event in self.hooks:
            for hook in self.hooks[ctx.event]:
                result: bool = await hook(ctx)
                if result:
                    pass
                else:
                    print(f"Hook: {hook}\nEvent: {ctx.event}\nError, hook did not run successfully")

    def on(self, event):
        def closure(func):
            self.hooks[event].append(func)
            return func
        return closure
