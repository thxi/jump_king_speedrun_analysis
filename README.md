# Jump king speedrun analysis

## Reproduce the results

The speedrun video should be 30fps, 60fps does not lead to an increase in quality

I used [this speedrun](https://youtu.be/FZ0fMGuJTLI) to manually extract screens from the game

0. `pip install -r requirements.txt`
1. Run `python3 download_video.py -l "https://youtu.be/FZ0fMGuJTLI" -o speedrun_side` to download the speedrun video to the `data` directory. This video will be used to map other videos.
2. (_Optional_) Run `python3 map_screens.py --video data/speedrun_side.mp4` and manually map the screens.

   - The repository already includes the file produced at this stage.
   - press `d` to map the start and `d` again to map the end of the screen

3. Run `python3 screen_to_frames.py --video data/speedrun_side.mp4` to obtain the `data/screen_to_frame.p`. This file stores the averaged frame for each screen for screen classification task in the next steps

4. Run `python3 heatmap.py --video path_to_video.mp4` to make the heatmap of the jump king for any other video
