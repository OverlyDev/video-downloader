import os
import pathlib
import re
import shutil

import yt_dlp
import ffmpeg


# Paths we need
CWD = pathlib.Path(__file__).parent.resolve()
INPUT_FILE = CWD / "urls.txt"
DOWNLOAD_DIR = pathlib.Path("/dev/shm/ytdlp-temp")
SAVE_DIR = CWD / "celeb"
YTDL_ARCHIVE = CWD / "ytdl_archive.txt"


def create_download_dict() -> dict:
    """
    Reads in urls.txt and returns a dictionary in the format:

    {<key number>:
        {
            'url': <video url>
            'title': <video title>
        }
    }
    """
    created_dict = {}
    with open(INPUT_FILE, "r") as f:
        raw = f.read()

    count = 0
    for line in raw.splitlines():
        if count not in created_dict:
            created_dict[count] = {}

        if line.startswith("#") or line == "":
            pass

        if line.startswith("https"):
            created_dict[count]["url"] = line
            count += 1

        else:
            created_dict[count]["title"] = line

    return created_dict


def extract_date_from_title(title: str) -> str:
    """Finds date in string (format: mm/dd/yy) and returns the date (format: mm-dd-yy)"""
    match_expr = r"\A[0-9]{1,2}[/][0-9]{1,2}[/][0-9]{1,2}"
    match = re.match(match_expr, title)
    if match is None:
        return ""
    else:
        return match.group().replace("/", "-")


def extract_just_the_title(x: str) -> str:
    """Returns the title without the date"""
    return x.split(": ")[1]


class MoveAndRenamePostProcessor(yt_dlp.postprocessor.PostProcessor):
    """
    A pretty jank post-processor for ytdlp

    1. Grabs the filename as downloaded by ytdlp
    2. Grabs the extension of above file
    3. Uses the url given to ytdlp to lookup the desired filename via url_to_title dict
    4. Moves downloaded file to save folder, using desired filename and ytdlp given extension
    """

    def run(self, info):
        # grab the path to the ytdlp downloaded file
        old_file = pathlib.Path(info["_filename"])

        # grab the extension from the ytdlp downloaded file
        extension = os.path.splitext(old_file)[1]

        # the url given to ytdlp
        webpage_url = info["webpage_url"]

        # new filename in actual save directory, with ytdlp given extension
        new_file = url_to_title_dict[webpage_url] + extension
        new_path = pathlib.Path(SAVE_DIR / new_file)

        # move file from temp to save folder
        shutil.move(old_file, new_path)

        return [], info


def main():
    # setup ytdlp opts
    ydl_opts = {
        "paths": {"home": str(DOWNLOAD_DIR)},
        "download_archive": str(YTDL_ARCHIVE),
    }

    # instantiate ytdlp and add our post-processor
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    ydl.add_post_processor(MoveAndRenamePostProcessor(), when="post_process")

    # populate our download_dict
    download_dict = create_download_dict()

    # start processing
    for _, v in download_dict.items():
        date = extract_date_from_title(v["title"])
        title = "Celebrity Jeopardy! - " + extract_just_the_title(
            v["title"] + f" ({date})"
        )
        url = v["url"]

        # create link of video url to desired title/filename (for our post-processor)
        url_to_title_dict[url] = title

        try:
            ydl.download([url])
        except yt_dlp.DownloadError:
            print(f"error downloading: {title} {url}")

    # convert any non-mp4 videos to mp4
    for f in pathlib.Path.iterdir(SAVE_DIR):
        if os.path.splitext(f)[1] != ".mp4":
            new_file = pathlib.Path(f).with_suffix(".mp4")
            print(f"converting: {f} -> {new_file}")
            (
                ffmpeg
                .input(str(f))
                .output(str(new_file), loglevel="fatal")    # Only show fatal errors
                .run()
            )

            # check if we have an mp4 of the offending file. if so, delete the non mp4
            if pathlib.Path.exists(new_file):
                os.remove(f)


if __name__ == "__main__":
    # this is in the global namespace so that the post-processor can access it
    url_to_title_dict = {}

    # create the folder that will contain final downloaded/renamed files
    pathlib.Path.mkdir(SAVE_DIR, exist_ok=True)

    # do things
    main()
