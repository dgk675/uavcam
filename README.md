# UAVCam

## Setup
1. Flash a Micro SD card with Raspberry Pi OS and boot it up.
2. Update the image using
    ```sh
    sudo apt-get update
    sudo apt-get upgrade -y
    ```
3. Install python dependencies
    ```sh
    pip install loguru tomli yamspy
    ```

## Configuration
Configuration is done via `config.toml`. Supported fields are:

### msp_port
The serial port on which to communicate with the flight controller \
`default: "/dev/ttyACM0"`

### msp_baudrate
The baudrate for communication with the flight controller\
`default: 115200`

### msp_photo_channel
The RC channel that triggers a photo\
`default: 12`

### msp_photo_threshold
The minimum value at which `msp_photo_channel` will trigger a photo\
`default: 1750`

### msp_video_channel
The RC channel that triggers a video\
`default: 11`

### msp_video_threshold
The minimum value at which `msp_video_channel` will trigger a video\
`default: 1750`

### output_path
Path, where the captured files will be saved\
`default: "./captures"`


## Converting captured videos
Captured videos are stored in .h264, as they are provied by picamera2. To convert them to mp4, simply run the included script:
```sh
convert_viedos.sh
```


