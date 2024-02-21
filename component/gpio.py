import datetime
from typing import Callable
import gpiozero


class GPIO:
    _button: gpiozero.Button
    _on_short_press: Callable
    _on_long_press: Callable
    _long_press_threshold: datetime.timedelta

    _start_timestamp: datetime.datetime

    def __init__(
        self,
        pin: int,
        *,
        on_short_press: Callable,
        on_long_press: Callable,
        long_press_threshold_ms: int = 5000
    ):
        self._button = gpiozero.Button(pin)
        self._on_short_press = on_short_press
        self._on_long_press = on_long_press
        self._long_press_threshold = datetime.timedelta(
            milliseconds=long_press_threshold_ms
        )
