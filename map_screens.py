import cv2
import pandas as pd

cap = cv2.VideoCapture('data/speedrun.mp4')

print("are you sure you want to overwrite frames dataframe?")
_ = input()


# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")
    exit(1)


fps = cap.get(cv2.CAP_PROP_FPS)
print(f"FPS: {fps}")
print(f"SPF: {1000/fps}")

frames_data = []
i = 0
mark_start = True
current_start = ()
screen_n = 0

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # d to mark the start
        k = cv2.waitKey(int(10)) & 0xFF
        if k == ord('d'):
            if mark_start:
                current_start = i
                print("start", i)
            else:
                frames_data.append((screen_n, current_start, i))
                print("end", i)
                print(screen_n)
                screen_n += 1
            mark_start = not(mark_start)

        # Press Q on keyboard to exit
        if k == ord('q'):
            break

        i += 1

        # Break the loop if something is wrong
    else:
        break


# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

frames_df = pd.DataFrame(frames_data, columns=["screen", "start", "end"])
frames_df.to_csv('data/screen_frames_info.csv', index=False)
