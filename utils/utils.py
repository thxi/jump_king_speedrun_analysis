import cv2
import imutils
import numpy as np
from collections import defaultdict
from tqdm.auto import tqdm


def dist(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2


def open_video(filename):
    cap = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        exit(1)

    return cap


def get_game_margins(cap):
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, length // 2)

    ret, frame = cap.read()
    count_left = 0
    for pixel in frame[0]:
        if (pixel == [0, 0, 0]).all():
            count_left += 1
        else:
            break

    count_right = 0
    for pixel in np.flip(frame[0], axis=0):
        if (pixel == [0, 0, 0]).all():
            count_right += 1
        else:
            break
    return count_left, count_right


def crop_margins(frame, margin_left, margin_right):
    return frame[:, margin_left:frame.shape[1] - margin_right]


def map_frames(filename, screen_to_frame):
    cap = open_video(filename)

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

    if start_frame_idx == -1:
        print(f"video {filename}, start_frame_idx is -1")
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
        if ret == True:
            frame = crop_margins(frame, margin_left, margin_right)
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
