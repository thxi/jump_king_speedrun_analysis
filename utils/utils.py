import cv2


def open_video(filename):
    cap = cv2.VideoCapture(filename)
    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        exit(1)

    return cap