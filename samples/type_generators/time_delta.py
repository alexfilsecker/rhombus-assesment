from random import choice, randint, random

TIME_DELTA_UNITS = [
    # Weeks
    "W",
    "D",
    # Days
    "days",
    "day",
    # Hours
    "hours",
    "hr",
    "h",
    # Minutes
    "minutes",
    "minute",
    "min",
    "m",
    # Seconds
    "seconds",
    "second",
    "s",
    # Milliseconds
    "milliseconds",
    "millisecond",
    "millis",
    "milli",
    "ms",
    # Microseconds
    "microseconds",
    "microsecond",
    "micros",
    "micro",
    "us",
    # Nanoseconds
    "nanoseconds",
    "nanosecond",
    "nanos",
    "nano",
    "ns",
]


def random_time_delta():
    unit = choice(TIME_DELTA_UNITS)
    value = random() * randint(1, 100)
    return f"{value} {unit}"


def time_delta_generator():
    return ("timedelta", random_time_delta)
