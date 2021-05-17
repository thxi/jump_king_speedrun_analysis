import cv2
import imutils
import numpy as np
from tqdm.auto import tqdm

from utils.utils import crop_margins, get_game_margins


# used to obtain a finer version of screen_to_frame
# for future use
def get_screen_to_frame(cap, screen_to_frames):
    margin_left, margin_right = get_game_margins(cap)
    # make new screen to frame
    print("making screen to frame for video")
    screen_to_frame = {}
    for screen, frames in tqdm(screen_to_frames.items()):
        start, end = frames[0]
        n = end - start
        cap.set(cv2.CAP_PROP_POS_FRAMES, start)
        frames = []
        for _ in range(n):
            ret, frame = cap.read()
            if ret == False:
                break

            frame = crop_margins(frame, margin_left, margin_right)
            frame = imutils.resize(frame, width=600)
            frame = cv2.resize(frame, (600, 450))
            frames.append(frame)

        avg_frame = np.mean(frames, axis=0)
        screen_to_frame[screen] = avg_frame.astype(np.uint8)
    return screen_to_frame
