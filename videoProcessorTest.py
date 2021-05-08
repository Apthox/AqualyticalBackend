import cv2
import pandas as pd
import json
from vidstab import VidStab
import os

filename = 'V3136'

df_events = pd.DataFrame()
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*'VP90')

video_in = cv2.VideoCapture(f'./imports/{filename}.mp4')
width = video_in.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video_in.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = video_in.get(cv2.CAP_PROP_FPS)

frames = video_in.get(cv2.CAP_PROP_FRAME_COUNT)
fps = int(video_in.get(cv2.CAP_PROP_FPS))

# calculate dusration of the video
seconds = int(frames / fps)

# Loads JSON track
with open(f'./imports/{filename}.json') as f:
    data = json.load(f)['data']['tracks']
    df_events = pd.json_normalize(data, 'events')
    df_events = df_events[df_events['time'] <= seconds]

    total = df_events.groupby('uuid').ngroups


track_uuid = 'c5fa1b73-6ee5-405f-948d-9ee7833c2c4f'
df_track = df_events[df_events['uuid'] == track_uuid].sort_values(by=['time'])

print(df_track)