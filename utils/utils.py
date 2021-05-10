import cv2
import numpy as np


def open_video(filename):
    cap = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        exit(1)

    return cap


def get_video_margins(cap):
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