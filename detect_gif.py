import argparse
import pickle
from collections import defaultdict

import cv2
import imutils
import imageio
import numpy as np
from tqdm.auto import tqdm

from utils.map_frames import map_frames
from utils.screen_to_frame import get_screen_to_frame
from utils.utils import crop_margins, get_game_margins, open_video, dist

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))

cap = open_video('data/speedrun_side.mp4')

screen_to_frames, frame_to_screen = map_frames(cap, screen_to_frame)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

screen_to_frame = get_screen_to_frame(cap, screen_to_frames)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

margin_left, margin_right = get_game_margins(cap)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

screen_to_positions = defaultdict(list)  # {screen: [[x, y]]}
positions = []

images = []
print("getting king's positions")
for screen, frames in tqdm(screen_to_frames.items()):
    avg_frame = screen_to_frame[screen]
    avg_frame = cv2.cvtColor(avg_frame, cv2.COLOR_BGR2GRAY)
    avg_frame = imutils.resize(avg_frame, width=60)
    for (start, end) in frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        if len(positions) != 0:
            x, _ = positions[-1]
            screen_positions = [(x, frame.shape[0])]
        else:
            screen_positions = [(30, 40)]

        n = end - start
        for _ in range(n):
            ret, frame = cap.read()
            if ret == False:
                break

            frame = crop_margins(frame, margin_left, margin_right)
            orig_side = frame.copy()
            orig_side = imutils.resize(orig_side, width=200)
            # orig_side = cv2.resize(orig_side, (600, 450))
            frame = imutils.resize(frame, width=60)
            orig_frame = frame.copy()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_diff = cv2.absdiff(avg_frame, frame)

            ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
            dilate_frame = cv2.dilate(thres, None, iterations=2)

            contours, _ = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                # draw candidates
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 0, 255),
                              1)

            if len(contours) == 0:
                # screen_positions.append(screen_positions[-1])
                pass
            elif len(contours) == 1:
                (x, y, w, h) = cv2.boundingRect(contours[0])
                if dist(screen_positions[-1], (x + w // 2, y + h // 2)) > 200:
                    # detected another object
                    screen_positions.append(screen_positions[-1])
                else:
                    screen_positions.append((x + w // 2, y + h // 2))
            else:
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

            orig_frame = imutils.resize(orig_frame, width=200)
            orig_frame = np.concatenate((orig_side, orig_frame), axis=1)
            cv2.imshow('frame', orig_frame)

            orig_frame = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGB)
            images.append(orig_frame)
            k = cv2.waitKey(25) & 0xFF
            if k == ord('q'):
                break
            if k == ord('d'):
                print(len(images))
                imageio.mimsave('data/detect_gif.gif', images, duration=0.03)
                exit(1)

cv2.destroyAllWindows()
cap.release()