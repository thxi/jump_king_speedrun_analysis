import pickle
from utils.utils import open_video
import numpy as np
import imutils
import cv2
from collections import defaultdict
from tqdm.auto import tqdm

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))
screen_to_frame = np.array(
    [imutils.resize(v, width=60).ravel() for v in screen_to_frame.values()])

cap = open_video('data/speedrun.mp4')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# get video start
start_frame_idx = -1  # count from 0
num_of_screen_0 = 0
i = -1
for _ in tqdm(range(length)):
    i += 1
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=60).ravel()
        distances = np.sum((screen_to_frame - frame)**2, axis=1)
        screen = np.argmin(distances)
        if screen == 0:
            num_of_screen_0 += 1
        else:
            num_of_screen_0 = 0
        if num_of_screen_0 == 10:  # at least 10 screens to be sure
            start_frame_idx = i
            break
    else:
        print("something went wrong")
        exit(1)

print(f"video starts at frame {start_frame_idx}")

# move to start
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_idx)

# get dictionary {screen: [frames]}
# get array [screen_n, screen_n, screen_n]
screen_to_frames = defaultdict(list)  # {[(start, end+1)]} dictionary of arrays
frame_to_screen = [-1] * start_frame_idx

prev_screen = 0
start = start_frame_idx

i = start_frame_idx
# for _ in tqdm(range(length - start_frame_idx)):
for _ in tqdm(range(1000)):
    ret, frame = cap.read()
    if ret == True:
        frame = imutils.resize(frame, width=60).ravel()
        distances = np.sum((screen_to_frame - frame)**2, axis=1)
        screen = np.argmin(distances)
        if screen != prev_screen:
            screen_to_frames[prev_screen].append((start, i))
            prev_screen = screen
            start = i
        frame_to_screen.append(screen)
        i += 1
    else:
        print("something went wrong")
        exit(1)

screen_to_frames[screen].append((start, i))

cap.release()
print("done mapping screens")
print(screen_to_frames[0])
print(frame_to_screen[678:800])
