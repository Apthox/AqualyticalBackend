import cv2
import pandas as pd
import json
import random
import os
import copy
from shutil import copyfile

def process(filename):

    if not (os.path.exists('./imports/' + filename + '.mov') and os.path.exists('./imports/' + filename + '.json')):
        print('Files not found for given filename!')
        return

    # Overlay video with events
    df_events = pd.DataFrame()
    df_summary = pd.DataFrame()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_in = cv2.VideoCapture('./imports/' + filename + '.mov')
    width = int(video_in.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video_in.get(cv2.CAP_PROP_FPS)

    # Loads JSON track
    with open('./imports/' + filename + '.json') as f:
        data = json.load(f)['data']['tracks']
        df_events = pd.json_normalize(data, record_path=['events'])

    # print(df_events.track_id.unique())

    # evt_video_out = cv2.VideoWriter('V3136_20071206T211301Z_16-20-58-06TC_h264-0-1-min-overlay.mov', fourcc=fourcc, fps=fps, frameSize=(width, height))

    # print(df_events.info())
    # Sort events in time order
    df_events = df_events.sort_values(by=['time'])

    if not os.path.isdir('./exports/' + filename):
        os.mkdir('./exports/' + filename)

    copyfile('./imports/' + filename + '.mov', './exports/' + filename + '/source.mov')
    copyfile('./imports/' + filename + '.json', './exports/' + filename + '/source.json')

    vid_time = 0.0
    spf = 1.0/fps
    f = 0
    while True:
        f = f + 1
        ret, frame = video_in.read()

        if not ret:
            break

        df = df_events[ (df_events['time'] <= vid_time + spf) & (df_events['time'] >= vid_time - spf) ]

        for row in df.iterrows():
            copy_frame = copy.deepcopy(frame)
            print(f'found {len(df)} events at {vid_time} seconds')
            cv2.rectangle(copy_frame, (row[1].x, row[1].y), (row[1].x+row[1].width, row[1].y+row[1].height), (255, 0, 0), 2)
            directory = './exports/' + filename + '/' + str(row[1]['uuid'])

            if not os.path.isdir(directory):
                os.mkdir(directory)

            cv2.imwrite(directory + '/frame-' + str(f) + '.jpg', copy_frame)

        vid_time += spf

    video_in.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    process('V3136')