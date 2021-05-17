import argparse
import sys

from pytube import YouTube


def progress(s, chunk, bytes_remaining):
    download_percent = int((s.filesize - bytes_remaining) / s.filesize * 100)
    sys.stdout.write(f'\rProgress: {download_percent} %\n')
    sys.stdout.flush()


ap = argparse.ArgumentParser()
ap.add_argument("-l", "--link", help="link to youtube video")
ap.add_argument("-o", "--out", help="output file name")
args = vars(ap.parse_args())

# https://youtu.be/FZ0fMGuJTLI to the side
# https://youtu.be/9_W-3lAljes centered
link = args.get("link", None)
if link is None:
    print("--link should be specified")
    exit(1)

filename = args.get("out", None)
if filename is None:
    print("--out should be specified")
    exit(1)

yt = YouTube(link, on_progress_callback=progress)

video = yt.streams.filter(subtype='mp4', fps=30)[0]
video.download('data', filename=filename)
