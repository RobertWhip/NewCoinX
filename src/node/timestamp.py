from datetime import datetime


def now() -> int:
    return datetime.now().timestamp()