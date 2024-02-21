import tomli

import time
from yamspy import MSPy
from loguru import logger

from component.camera import Camera, ExifGpsData


def on_short_press():
    logger.debug("short press detected")


def on_long_press():
    logger.debug("long press detected")


def process_command(board: MSPy, command: str):
    if board.send_RAW_msg(MSPy.MSPCodes[command], data=[]):
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)


if __name__ == "__main__":
    # load config
    with open("config.toml", "rb") as f:
        config = tomli.load(f)

    # initialize camera module
    logger.debug("Setting up camera module")
    camera = Camera(output_path=config["output_path"])

    previous_rc_high = False

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
            logger.trace(board.RC["channels"])
            logger.trace(board.GPS_DATA)

            # photo handling
            if (
                board.RC["channels"][config["msp_photo_channel"] - 1]
                >= config["msp_photo_threshold"]
            ):
                if not previous_rc_high:
                    gps_data = None

                    if board.GPS_DATA["fix"]:
                        gps_data = ExifGpsData(
                            latitude=board.GPS_DATA["lat"] * 1e-07,
                            longitude=board.GPS_DATA["lon"] * 1e-07,
                            altitude=board.GPS_DATA["alt"],
                            speed=board.GPS_DATA["speed"] * 1e-01,
                            heading=board.GPS_DATA["ground_course"] * 1e-01,
                        )
                    camera.capture_photo(gps_data)
                    previous_rc_high = True
            else:
                previous_rc_high = False

            # video handling
            if (
                board.RC["channels"][config["msp_video_channel"] - 1]
                >= config["msp_video_threshold"]
            ):
                if not camera.is_recording:
                    camera.start_recording()
            else:
                if camera.is_recording:
                    camera.stop_recording()
