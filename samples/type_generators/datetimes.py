import datetime
from random import choice, randrange


def random_datetime():
    start = datetime.datetime(1970, 1, 1)
    end = datetime.datetime.now()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


DATE_TIME_FORMATS = [
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%B %d %Y",
    "%b %d %Y",
    "%I:%M:%S %p",
    "%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %I:%M:%S",
]


def random_datetime_str(format: str):
    def inner():
        # rand_datetime = random_datetime()
        rand_datetime = datetime.datetime.now()
        return rand_datetime.strftime(format)

    return inner


def datetime_generator():
    format = choice(DATE_TIME_FORMATS)
    return (f"datetime({format})", random_datetime_str(format))
