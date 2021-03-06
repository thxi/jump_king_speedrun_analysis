# Jump king speedrun analysis

![detect.gif](data/detect_gif.gif)

[Jump King](https://store.steampowered.com/app/1061090/Jump_King/) is a challenging climbing-platformer. The speedrun, however, [takes under 5 minutes of time](https://www.speedrun.com/jumpking) which makes it possible to perform quick feature extraction from the speedrun videos.

In this project I decode the raw videos of a game to extract useful features, such as current screen (i.e. stage or background) and king's position.
As a result, I obtain [the heatmap](https://imgur.com/a/Jc0KOA4) from the video data alone.
The data can be used for further analysis such as the number of falls made on each stage so that the players would know the areas which they need to train more.

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

## Heatmap

See [full image](https://i.imgur.com/Tfp4rag.jpg)

![image.png](data/heatmap_crop.png)
