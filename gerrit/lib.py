import os

def dprint(*args):
    if os.environ.get("LOG_LEVEL", "INFO") == "DEBUG":
        print(*args)
