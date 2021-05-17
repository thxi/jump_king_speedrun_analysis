import argparse
import pickle

import cv2
import numpy as np
from tqdm.auto import tqdm

from utils.detect_king import get_king_positions
from utils.heatmap import make_heatmap
from utils.map_frames import map_frames
from utils.screen_to_frame import get_screen_to_frame
from utils.utils import open_video

screen_to_frame = pickle.load(open("data/screen_to_frame.p", "rb"))

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

cap = None
video = args.get("video", None)
if video is None:
    print("--video should be specified")
    exit(1)
else:
    cap = open_video(video)

screen_to_frames, frame_to_screen = map_frames(cap, screen_to_frame)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

screen_to_frame = get_screen_to_frame(cap, screen_to_frames)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

positions, screen_to_positions = get_king_positions(cap, screen_to_frames,
                                                    screen_to_frame)
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

print("drawing the heatmap")
screen_to_heatmap = {}
for i in tqdm(range(43)):
    heatmap = make_heatmap(screen_to_positions[i], screen_to_frame[i])
    screen_to_heatmap[i] = heatmap

im = np.concatenate([screen_to_heatmap[i] for i in range(43)][::-1], axis=0)

cv2.imwrite('data/heatmap.png', im)

cap.release()
