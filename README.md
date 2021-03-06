## Setup
1. `./setup.sh` Run setup.sh to install apt requirements, create a virtual environment, and install pip packages
2. `source venv/bin/activate` Activate virtual environment

## Usage
1. `python3 main.py`
2. Videos will be downloaded to /dev/shm, renamed, and moved into \<cwd\>/celeb
3. Any videos that are not in .mp4 format will be converted to .mp4

## Notes
yt-dlp is currently configured to use an archive file: `<cwd>/ytdl_archive.txt`. Meaning, once a file is downloaded it won't be downloaded again.
You can either delete the archive file to re-download or disable the functionality by commenting out [this](https://github.com/OverlyDev/video-downloader/blob/7fa1ba0ecec7d2eb45d7732f437b90fb8fa45c1b/main.py#L100) line.

Currently there's a couple hard-coded functions specifc to my use case. These might become more generic in the future

The original funnyjunk urls were incompatible with yt-dlp so I had to inspect the webpage source and grab the actual video url. This might work for other unsupported sites.

## Compatibility
This was created and tested on PopOS 22.04 (python 3.10) and thus the apt-requirements.txt reflects the packages used on that OS. 

If you're using a different OS/python version, you may need to modify the apt-requirements.txt for it to work. 

No guarantees for older/newer python versions.

### References:
https://github.com/yt-dlp/yt-dlp

https://github.com/kkroening/ffmpeg-python