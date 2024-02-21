import tomli

import time
from yamspy import MSPy
from loguru import logger

from component.camera import Camera
from component.gpio import GPIO


def on_short_press():
    logger.debug("short press detected")


def on_long_press():
    logger.debug("long press detected")


def process_command(board: MSPy, command: str):
    if board.send_RAW_msg(MSPy.MSPCodes[command], data=[]):
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomli.load(f)

    # if config["one_button"]:
    #     gpio_pin = config["one_button_pin"]
    #     gpio = GPIO(
    #         gpio_pin,
    #         on_short_press=on_short_press,
    #         on_long_press=on_long_press,
    #         long_press_threshold_ms=2000,
    #     )

    logger.debug("Setting up camera module")

    camera = Camera(output_path=config["output_path"])

    previous_rc_high = False

    # logger.debug("Taking photo")
    # camera.capture_photo()

    # logger.debug("Starting video capture")
    # camera.start_recording()

    # time.sleep(5)

    # camera.capture_photo()

    # time.sleep(5)

    # logger.debug("Stoppint video capture")
    # camera.stop_recording()

    with MSPy(
        device=config["msp_port"],
        loglevel="WARNING",
        baudrate=config["msp_baudrate"],
    ) as board:
        if board == 1:  # an error occurred...
            print("Not connected to the FC...")
            exit(1)

        while True:
            time.sleep(0.1)

            process_command(board, "MSP_RC")
            process_command(board, "MSP_RAW_GPS")
            print(board.RC["channels"])
            # print(board.GPS_DATA)

            if (
                board.RC["channels"][config["msp_rc_channel"] - 1]
                >= config["msp_rc_threshold"]
            ):
                if not previous_rc_high:
                    logger.debug("Capturing photo..")
                    camera.capture_photo()
                    previous_rc_high = True
            else:
                previous_rc_high = False
