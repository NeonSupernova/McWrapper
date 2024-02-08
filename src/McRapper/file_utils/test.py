from re import compile
from enum import Enum


class Levels(Enum):
    INFO = compile(r"\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\s\[(.*)/INFO]:\s(.*)")
    WARN = compile(r"\[([0-9]{2}:[0-9]{2}:[0-9]{2})]\s\[(.*)/WARN]:\s(.*)")


test_str = "[09:56:23] [ServerMain/INFO]: Loaded 7 recipes"

for lev in Levels:
    print(lev.value.match(test_str))
