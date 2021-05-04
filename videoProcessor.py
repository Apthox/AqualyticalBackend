import cv2
import pandas as pd
import json
from vidstab import VidStab

def processVideo(filename):
    stabilizer = VidStab()
    df_events = pd.DataFrame()
    df_summary = pd.DataFrame()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_in = cv2.VideoCapture('./imports/V3136.mov')
    width = video_in.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_in.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_in.get(cv2.CAP_PROP_FPS)

    # Loads JSON track
    with open('./imports/V3136.json') as f:
        data = json.load(f)['data']['tracks']
        df_events = pd.json_normalize(data, 'events')
        df_events = df_events[df_events['time'] < 60]

        def processTrack(df):
            df_frames = df.sort_values(by=['time'])
            # print(df)

            max_h = max(df_frames.height.max(), 100)
            max_w = max(df_frames.width.max(), 100)

            uuid = df.name

            evt_video_out = cv2.VideoWriter()
            evt_video_out.open(f'./exports/V3136/{uuid}/source.mov', fourcc, fps, frameSize=(max_w, max_h))

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
    processVideo('')