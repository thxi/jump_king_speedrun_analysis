# Jump king speedrun analysis

## Reproduce the results

0. `pip install -r requirements.txt`
1. Download a speedrun video
2. (_Optional_) Run `python3 map_screens.py --video path_to_video.mp4` and manually map the screens.

   - The repository already includes the file produced at this stage.
   - press `d` to map the start and `d` again to map the end of the screen

3. Run `python3 heatmap.py --video path_to_video.mp4` to make the heatmap of the jump king

TODO:
make a gif of detection
make heatmap
finish readme
