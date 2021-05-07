import pickle
from utils.utils import open_video
import numpy as np
import pandas as pd
import imutils
import cv2

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))
screen_to_frame = np.array(
    [imutils.resize(v, width=60).ravel() for v in screen_to_frame.values()])

start_frame_idx = -1  # from 0

cap = open_video('data/speedrun.mp4')
screen_0 = 0
i = -1
while (cap.isOpened()):
    i += 1
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=60).ravel()
        distances = np.sum((screen_to_frame - frame)**2, axis=1)
        screen = np.argmin(distances)
        if screen == 0:
            screen_0 += 1
        else:
            screen_0 -= 1
        if screen_0 == 10:  # at least 10 screens to be sure
            start_frame_idx = i

    else:
        break

# Mark video to screens

screen_to_zones = []  # (start, end+1)

# move to start
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_idx)

current_screen = 0
screen_start = start_frame_idx
i = start_frame_idx
prev_prev_scren = -1
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=60).ravel()
        distances = np.sum((screen_to_frame - frame)**2, axis=1)
        screen = np.argmin(distances)
        if screen == prev_prev_scren: # falling back 1 screen


        if screen != current_screen:
            screen_to_zones.append((screen_start, i))
            screen_start = i

    else:
        break

cap.release()