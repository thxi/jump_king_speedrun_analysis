import pandas as pd
import numpy as np

import cv2
import imutils
import pickle

from tqdm.auto import tqdm
from utils.utils import open_video

frames_df = pd.read_csv('data/screen_frames_info.csv')

cap = open_video('data/speedrun.mp4')

screen_to_frame = {}

for _, f in tqdm(frames_df.iterrows()):
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
        frames.append(frame)
    frames = np.array(frames)
    avg = np.mean(frames, axis=0)
    imutils.resize(avg, width=150)
    screen_to_frame[screen] = avg.astype(np.uint8)

cap.release()

pickle.dump(screen_to_frame, open("data/screen_to_frame.p", "wb"))