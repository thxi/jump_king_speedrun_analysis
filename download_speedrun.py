from pytube import YouTube

# yt = YouTube('https://youtu.be/9_W-3lAljes') # centered video
yt = YouTube('https://youtu.be/FZ0fMGuJTLI')  # to the side
# print('\n'.join([str(x) for x in yt.streams.filter(subtype='mp4', fps=60)]))

(yt.streams.filter(subtype='mp4')[0].download('data',
                                              filename='speedrun_side'))
