## Setup
1. `./setup.sh` Run setup.sh to install apt requirements, create a virtual environment, and install pip packages
2. `source venv/bin/activate` Activate virtual environment

## Usage
1. `python3 main.py`
2. Videos will be downloaded to /dev/shm, renamed, and moved into \<cwd\>/celeb
3. Any videos that are not in .mp4 format will be converted to .mp4

## Notes
Currently there's a couple hard-coded functions specifc to my use case. These might become more generic in the future

The original funnyjunk urls were incompatible with yt-dlp so I had to inspect the webpage source and grab the actual video url. This might work for other unsupported sites.

### References:
https://github.com/yt-dlp/yt-dlp

https://github.com/kkroening/ffmpeg-python