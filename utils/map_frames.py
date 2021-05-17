import cv2
import imutils
import numpy as np
from collections import defaultdict
from tqdm.auto import tqdm

from .utils import open_video, get_game_margins, crop_margins


# map each frame in the video
# i.e. to which screen a frame belongs
def map_frames(cap, screen_to_frame):
    screen_to_frame = np.array([v.ravel() for v in screen_to_frame.values()])

    margin_left, margin_right = get_game_margins(cap)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("getting video start")
    # get video start
    start_frame_idx = -1  # count from 0
    num_of_screen_0 = 0
    i = -1
    for _ in tqdm(range(length)):
        i += 1
        ret, frame = cap.read()
        if ret == True:
            frame = crop_margins(frame, margin_left, margin_right)
            frame = imutils.resize(frame, width=60)
            frame = cv2.resize(frame, (60, 44)).ravel()

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

    if start_frame_idx == -1:
        print(f"start_frame_idx is -1")
        exit(228)
    print(f"video starts at frame {start_frame_idx}")

    print("mapping screens")
    # move to start
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_idx)

    # get dictionary {screen: [frames]}
    # get array [screen_n, screen_n, screen_n]
    screen_to_frames = defaultdict(
        list)  # {[(start, end+1)]} dictionary of arrays
    frame_to_screen = [-1] * start_frame_idx

    prev_screen = 0
    start = start_frame_idx

    i = start_frame_idx
    for _ in tqdm(range(length - start_frame_idx)):
        ret, frame = cap.read()
        if not (ret):
            print("could not map screens, ret=False")
            exit(1)
        frame = crop_margins(frame, margin_left, margin_right)
        frame = imutils.resize(frame, width=60)
        frame = cv2.resize(frame, (60, 44)).ravel()
        distances = np.sum((screen_to_frame - frame)**2, axis=1)
        screen = np.argmin(distances)
        if screen != prev_screen:
            screen_to_frames[prev_screen].append((start, i))
            prev_screen = screen
            start = i
        frame_to_screen.append(screen)
        i += 1

    screen_to_frames[screen].append((start, i))

    # special case for the ending screen
    # when detected more frames than needed
    xy = screen_to_frames[42][0]
    screen_to_frames[42][0] = (xy[0], xy[0] + 140)

    # usually there is an ending screen in video
    # this removes incorrectly classified frames
    last_frame = screen_to_frames[42][0][1] - 1  # last frame of last screen
    frame_to_screen = np.array(frame_to_screen)
    frame_to_screen[last_frame:] = -1
    for k, s in screen_to_frames.items():
        to_delete = -1
        for i in range(len(s)):
            if s[i][0] > last_frame:
                to_delete = i
        if to_delete != -1:
            screen_to_frames[k] = s[:to_delete]

    return screen_to_frames, frame_to_screen
