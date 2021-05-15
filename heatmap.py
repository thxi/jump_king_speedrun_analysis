import pickle

import cv2
import numpy as np

from utils.detect_king import get_king_positions
from utils.heatmap import make_heatmap
from utils.map_frames import map_frames
from utils.screen_to_frame import get_screen_to_frame
from utils.utils import open_video

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))
screen_to_frame = np.array([v.ravel() for v in screen_to_frame.values()])

screen_to_frames, frame_to_screen = map_frames('data/speedrun_side.mp4',
                                               screen_to_frame)

cap = open_video('data/speedrun_side.mp4')
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

screen_to_frame = get_screen_to_frame(cap, screen_to_frames)

positions, screen_to_positions = get_king_positions(cap, screen_to_frames,
                                                    screen_to_frame)

i = 1
heatmap = make_heatmap(screen_to_positions[i], screen_to_frame[i])

cv2.imshow("frame", heatmap)