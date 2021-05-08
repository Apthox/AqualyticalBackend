import cv2
import pandas as pd
import json
from vidstab import VidStab
import os

count = 0
total = 0

def processVideo(filename):
    stabilizer = VidStab()
    df_events = pd.DataFrame()
    df_summary = pd.DataFrame()
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
    print(f'length: {seconds} seconds')

    if not os.path.isdir('./exports/' + filename):
        os.mkdir('./exports/' + filename)

    # Loads JSON track
    with open(f'./imports/{filename}.json') as f:
        data = json.load(f)['data']['tracks']
        df_events = pd.json_normalize(data, 'events')
        df_events = df_events[df_events['time'] <= seconds]

        total = df_events.groupby('uuid').ngroups

        def processTrack(df):
            global count
            count = count + 1

            print(f'{count} / {total}')

            df_frames = df.sort_values(by=['time'])
            # print(df)

            max_h = max(df_frames.height.max(), 100)
            max_w = max(df_frames.width.max(), 100)

            uuid = df.name

            if not os.path.isdir(f'./exports/{filename}/{uuid}'):
                os.mkdir(f'./exports/{filename}/{uuid}')
            
            row = df_frames[df_frames['surprise']==df_frames['surprise'].max()]
            frame = round(row.time.values[0] * fps)
            video_in.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ret, frame = video_in.read()
            x = int(row.x.values[0] - round((max_w - row.width.values[0])/2))
            y = int(row.y.values[0] - round((max_h - row.height.values[0])/2))
            crop = frame[y:y+max_h,x:x+max_w]
            cv2.imwrite(f'./exports/{filename}/{uuid}/thumbnail.png', crop)
            print('Image Generated!')

            evt_video_out = cv2.VideoWriter()
            evt_video_out.open(f'./exports/{filename}/{uuid}/source.webm', fourcc, fps, frameSize=(max_w, max_h))

            print(f'Creating video for {uuid} length {len(df_frames) / fps} seconds')
            print(max_h)
            print(max_w)
            print(df.name)

            for i, row in enumerate(df_frames.iterrows()):
                frame = round(row[1].time*fps)
                video_in.set(cv2.CAP_PROP_POS_FRAMES, frame)

                # calculate the adjusted crop size
                ret, frame = video_in.read()
                x = int(row[1].x - round((max_w - row[1].width)/2))
                y = int(row[1].y - round((max_h - row[1].height)/2))
                crop = frame[y:y+max_h,x:x+max_w]

                evt_video_out.write(crop)

                # try:
                #     if len(df) > 30:
                #         stabilized_frame = stabilizer.stabilize_frame(input_frame=crop, border_type='black', smoothing_window=30)
                #         if stabilized_frame.sum() > 0:
                #             evt_video_out.write(stabilized_frame)
                #     else:
                #         evt_video_out.write(crop)
                # except Exception as e:
                #     print('Stablization Failed')
                #     break
            
            print('----------------')

            evt_video_out.release()

    df_events.groupby('uuid').apply(processTrack)

if __name__ == '__main__':
    processVideo('V3136')