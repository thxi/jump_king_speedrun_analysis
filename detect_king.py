import numpy as np
import matplotlib.pyplot as plt

import cv2
import imutils
import pickle

from tqdm.auto import tqdm
from utils.utils import (open_video, get_game_margins, crop_margins, dist,
                         map_frames)

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))
screen_to_frame = np.array([v.ravel() for v in screen_to_frame.values()])

screen_to_frames, frame_to_screen = map_frames('data/speedrun_side.mp4',
                                               screen_to_frame)

cap = open_video('data/speedrun_side.mp4')
margin_left, margin_right = get_game_margins(cap)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# make new screen to frame
screen_to_frame = {}
for screen, frames in tqdm(screen_to_frames.items()):
    start, end = frames[0]
    n = end - start
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)
    frames = []
    for i in range(n):
        ret, frame = cap.read()
        if ret == False:
            break

        frame = crop_margins(frame, margin_left, margin_right)
        frame = imutils.resize(frame, width=60)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(frame)

    avg_frame = np.mean(frames, axis=0)
    screen_to_frame[screen] = avg_frame.astype(np.uint8)

screen_to_positions = {}  # {screen: [[x, y]]}
positions = []

# some screens are badly initialized

# if go back, then have to initialize screen_positions differently
# if go back, then have to jump to next frame first
for screen, frames in tqdm(screen_to_frames.items()):
    for (start, end) in frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        if len(positions) != 0:
            x, _ = positions[-1]
            screen_positions = [(x, frame.shape[0])]
        else:
            screen_positions = [(30, 40)]

        for i in range(n):
            print(screen)
            avg_frame = screen_to_frame[screen]
            ret, frame = cap.read()
            if ret == False:
                break

            frame = crop_margins(frame, margin_left, margin_right)
            frame = imutils.resize(frame, width=60)
            orig_frame = frame.copy()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(avg_frame, frame)

            # exponential smoothing
            # TODO: if needed
            # avg_frame = (0.3 * frame + 0.7 * avg_frame).astype(np.uint8)

            ret, thres = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)
            dilate_frame = cv2.dilate(thres, None, iterations=2)

            contours, hierarchy = cv2.findContours(dilate_frame,
                                                   cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # draw candidates
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 0, 255),
                              1)

            if len(contours) == 0:
                screen_positions.append(screen_positions[-1])
            elif len(contours) == 1:
                (x, y, w, h) = cv2.boundingRect(contours[0])
                if dist(screen_positions[-1], (x + w // 2, y + h // 2)) > 200:
                    print("more than 50")
                    # detected another object
                    screen_positions.append(screen_positions[-1])
                else:
                    # print("her")
                    screen_positions.append((x + w // 2, y + h // 2))
            else:
                # TODO: choose the one with more intersection
                distances = []
                for contour in contours:
                    (x, y, w, h) = cv2.boundingRect(contour)
                    distances.append(
                        dist(screen_positions[-1], (x + w // 2, y + h // 2)))
                pidx = np.argmin(distances)
                (x, y, w, h) = cv2.boundingRect(contours[pidx])
                screen_positions.append((x + w // 2, y + h // 2))

            x, y = screen_positions[-1]
            cv2.rectangle(orig_frame, (x - 3, y - 3), (x + 3, y + 3),
                          (0, 255, 0), 1)

            avg_frame = cv2.cvtColor(avg_frame, cv2.COLOR_GRAY2RGB)
            orig_frame = np.concatenate((orig_frame, avg_frame), axis=0)
            orig_frame = imutils.resize(orig_frame, width=600)
            cv2.imshow("view", orig_frame)
            k = cv2.waitKey(10) & 0xFF
            if k == ord('q'):
                exit(1)

        positions = positions + screen_positions

cv2.destroyAllWindows()