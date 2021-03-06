# used to obtain averaged frame for each screen
# need to run map_screens.py first
import argparse

import pandas as pd
import numpy as np

import cv2
import imutils
import pickle

from tqdm.auto import tqdm
from utils.utils import open_video, get_game_margins, crop_margins

frames_df = pd.read_csv('data/screen_frames_info.csv')

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

cap = None
video = args.get("video", None)
if video is None:
    print("--video should be specified")
    exit(1)
else:
    cap = open_video(video)

margin_left, margin_right = get_game_margins(cap)
print(margin_left, margin_right)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

screen_to_frame = {}

for i in tqdm(range(len(frames_df))):
    f = frames_df.iloc[i, :]
    screen = f['screen']
    start = f['start']
    end = f['end']
    n = end - start + 1  # how many frames to read
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    for i in range(n):
        ret, frame = cap.read()
        if ret != True:
            print("something went wrong")
            break
        frame = crop_margins(frame, margin_left, margin_right)
        frames.append(frame)

    frames = np.array(frames)
    avg = np.mean(frames, axis=0)
    avg = imutils.resize(avg, width=60)
    avg = cv2.resize(avg, (60, 44))
    screen_to_frame[screen] = avg.astype(np.uint8)

cap.release()

cv2.destroyAllWindows()

pickle.dump(screen_to_frame, open("data/screen_to_frame.p", "wb"))