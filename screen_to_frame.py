# used to obtain averaged frame for each screen
# need to run map_screens.py first
import pandas as pd
import numpy as np

import cv2
import imutils
import pickle

from tqdm.auto import tqdm
from utils.utils import open_video, get_game_margins, crop_margins

frames_df = pd.read_csv('data/screen_frames_info.csv')

cap = open_video('data/speedrun.mp4')

margin_left, margin_right = get_game_margins(cap)
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
    screen_to_frame[screen] = avg.astype(np.uint8)

cap.release()

pickle.dump(screen_to_frame, open("data/screen_to_frame.p", "wb"))