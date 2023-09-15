from enum import Enum

class CandleResolution(Enum):
    _1DAY = (1, "day")
    _4HOURS = (4, "hour")
    _1HOUR = (1, "hour")
    _30MINUTES = (30, "minute")
    _15MINUTES = (15, "minute")
    _5MINUTES = (5, "minute")
    _1MINUTE = (1, "minute")

    def __init__(self, multiplier, interval):
        self.multiplier: int = multiplier
        self.interval: str = interval

    def __str__(self):
        interval_string = ""
        
        if self.interval == "minute":
            interval_string = "MIN"
        elif self.interval == "hour":
            interval_string = "HOUR"
        else:
            interval_string = "DAY"

        if self.multiplier > 1:
            interval_string += 'S'

        return f"{self.multiplier}{interval_string}"