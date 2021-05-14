import numpy as np

import cv2
import pickle

from utils.utils import open_video, get_game_margins,
from utils.detect_king import get_king_positions
from utils.map_frames import map_frames

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))
screen_to_frame = np.array([v.ravel() for v in screen_to_frame.values()])

screen_to_frames, frame_to_screen = map_frames('data/speedrun_side.mp4',
                                               screen_to_frame)

cap = open_video('data/speedrun_side.mp4')
margin_left, margin_right = get_game_margins(cap)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

positions, screen_to_positions = get_king_positions(cap, screen_to_frames)
