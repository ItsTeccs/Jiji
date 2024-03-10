import math
from datetime import datetime, timezone, timedelta


def apiTimeStrMalformed(str):
    # some gitlab api actions return malformed ISO data.
    # strings look like "2024-03-10 16:39:35 UTC"
    # eval the string and see if it is of malformed type.
    return str[0:len(str) - 4].strip().find("T") == -1


def apiTimeStrToIso(str):
    # gitlab api returns malformed ISO strings despite docs saying they are of ISO format.
    # strings look like "2024-03-10 16:39:35 UTC"
    # this function converts this malformed string into a valid iso format string such as 2019-03-15T08:00:00Z
    str = str[0:len(str) - 4].strip().replace(" ", "T") + "Z"
    return str


def getDeltaIsoMinutes(t0):
    # gets the time difference to UTC now() of a iso format string.
    t0 = datetime.fromisoformat(t0)
    t1 = datetime.now(tz=timezone.utc)

    print(t0)
    print(t1)

    delta = t1 - t0
    return math.floor(delta.seconds / 60)


def getDeltaIsoTime(t0):
    # get the datetime delta between the given t0 datetime string and datetime.now()
    t0 = datetime.fromisoformat(t0).astimezone(timezone.utc)
    t1 = datetime.now(tz=timezone.utc)
    delta = t1 - t0
    return delta
