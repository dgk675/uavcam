import tomli
import time
import RPi.GPIO as gpio
from loguru import logger

from component.camera import Camera


def on_button_detected():
    pass


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomli.load(f)

    if config["one_button"]:
        gpio_pin = config["one_button_pin"]
        gpio.setmode(gpio.BCM)
        gpio.setup(gpio_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

        gpio.add_event_detect(gpio_pin, gpio.FALLING, callback=on_button_detected)

    logger.debug("Setting up camera module")

    camera = Camera(output_path=config["output_path"])

    logger.debug("Taking photo")
    camera.capture_photo()

    logger.debug("Starting video capture")
    camera.start_recording()

    time.sleep(5)

    camera.capture_photo()

    time.sleep(5)

    logger.debug("Stoppint video capture")
    camera.stop_recording()
