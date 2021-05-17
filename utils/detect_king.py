from collections import defaultdict

import cv2
import imutils
import numpy as np
from tqdm.auto import tqdm

from utils.utils import crop_margins, dist, get_game_margins


# get positions for each screen
def get_king_positions(cap, screen_to_frames, screen_to_frame):
    margin_left, margin_right = get_game_margins(cap)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    screen_to_positions = defaultdict(list)  # {screen: [[x, y]]}
    positions = []

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
                frame = imutils.resize(frame, width=60)
                orig_frame = frame.copy()

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_diff = cv2.absdiff(avg_frame, frame)

                ret, thres = cv2.threshold(frame_diff, 50, 255,
                                           cv2.THRESH_BINARY)
                dilate_frame = cv2.dilate(thres, None, iterations=2)

                contours, _ = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

                if len(contours) == 0:
                    # screen_positions.append(screen_positions[-1])
                    pass
                elif len(contours) == 1:
                    (x, y, w, h) = cv2.boundingRect(contours[0])
                    if dist(screen_positions[-1],
                            (x + w // 2, y + h // 2)) > 200:
                        # detected another object
                        screen_positions.append(screen_positions[-1])
                    else:
                        screen_positions.append((x + w // 2, y + h // 2))
                else:
                    distances = []
                    for contour in contours:
                        (x, y, w, h) = cv2.boundingRect(contour)
                        distances.append(
                            dist(screen_positions[-1],
                                 (x + w // 2, y + h // 2)))
                    pidx = np.argmin(distances)
                    (x, y, w, h) = cv2.boundingRect(contours[pidx])
                    screen_positions.append((x + w // 2, y + h // 2))

                x, y = screen_positions[-1]

            positions = positions + screen_positions
            screen_to_positions[screen] += screen_positions
    return positions, screen_to_positions
