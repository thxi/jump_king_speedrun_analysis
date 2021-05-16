# used to map frames to screens manually
# so that each screen can be extracted from the game
# by averaging the frames within each screen
import argparse

import cv2
import pandas as pd

from utils.utils import open_video

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

print("are you sure you want to overwrite frames dataframe?",
      "Press Enter if you want to continue",
      "Press Ctrl+C to abort",
      sep='\n')
_ = input()

frames_data = []
i = 0
mark_start = True
current_start = ()
screen_n = 0

while (cap.isOpened()):
    ret, frame = cap.read()
    if not (ret):
        print("something went wrong")
        exit(1)

    cv2.imshow('Frame', frame)

    # d to mark the start
    k = cv2.waitKey(15) & 0xFF
    if k == ord('d'):
        if mark_start:
            current_start = i
            print("start", i)
        else:
            frames_data.append((screen_n, current_start, i))
            print("end", i)
            print(screen_n)
            screen_n += 1
        mark_start = not (mark_start)

    # q to exit
    if k == ord('q'):
        break

    i += 1

cap.release()

cv2.destroyAllWindows()

frames_df = pd.DataFrame(frames_data, columns=["screen", "start", "end"])
frames_df.to_csv('data/screen_frames_info.csv', index=False)
