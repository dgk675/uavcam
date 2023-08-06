from picamera2 import Picamera2
from picamera2.encoders import Encoder, H264Encoder, Quality
from loguru import logger
from pathlib import Path


class Camera:
    _picam2: Picamera2 = Picamera2()
    _encoder: Encoder = H264Encoder()
    _is_recording: bool = False
    _capture_config: dict
    _output_path: str
    _image_count: int
    _video_count: int

    def __init__(self, output_path) -> None:
        self._capture_config = self._picam2.create_still_configuration(
            raw={},
            display=None,
        )
        video_config = self._picam2.create_video_configuration()
        self._picam2.configure(video_config)

        # Ensure output path exists
        self._output_path = Path(output_path)
        self._output_path.mkdir(parents=True, exist_ok=True)

        # initialize file name counter
        files = [p.name for p in self._output_path.glob("IMG*")]
        if files:
            files.sort()
            self._image_count = int(files[-1].split(".")[0].lstrip("IMG"))
        else:
            self._image_count = 0

    @property
    def next_image(self):
        self._image_count += 1
        return f"IMG{self._image_count:05d}"

    def capture_photo(self):
        if self._is_recording:
            logger.error(
                "Can't capture stills while recording a video. Please stop the recording first."
            )
            return
        next_image = self.next_image
        logger.debug(f"Capturing photo {next_image}")
        self._picam2.start()
        r = self._picam2.switch_mode_and_capture_request(self._capture_config)
        r.save("main", f"{self._output_path}/{next_image}.jpg")
        r.save_dng(f"{self._output_path}/{next_image}.dng")
        self._picam2.stop()

    def start_recording(self):
        next_image = self.next_image
        logger.debug(f"Starting recording {next_image}")
        self._is_recording = True
        self._picam2.start_recording(
            self._encoder,
            f"{self._output_path}/{next_image}.h264",
            quality=Quality.HIGH,
        )

    def stop_recording(self):
        logger.debug("Stopping recording")
        self._picam2.stop_recording()
        self._picam2.stop()
        self._is_recording = False
