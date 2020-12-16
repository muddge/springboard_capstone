import os, csv
import cv2
import pandas as pd
import numpy as np
import time
path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/ground-truth-in-yolo-format'
video_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground'
save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/transfer-learning/data/images'

files = os.listdir(path)
video_files = os.listdir(video_path)

for f in files:

    if f.startswith('VIRAT_S_000002'):

        filename = path + '/' + f

        frames_df = pd.read_csv(filename, sep=' ', header=0, names=['class','x_center','y_center','box_width',
                                                                    'box_height','frame'])

        video_filename = video_path + '/' + f.split('.')[0] + '.mp4'

        frame_list = frames_df['frame'].tolist()
        frame_list = frame_list[::9]

        cap = cv2.VideoCapture(video_filename)

        frame_no = 0

        while cap.isOpened():

            start = time.time()
            saved_filename = save_path + '/' + f.split('.')[0] + '/' + f.split('.')[0] + '-' + str(frame_no) + '.jpg'
            cap.set(1,frame_no)
            ret, frame = cap.read()
            if ret == False:
                break
            cv2.imwrite(saved_filename, frame)
            elapsed = str(time.time() - start)
            print(saved_filename + " " + elapsed + " seconds")
            frame_no += 1

        cap.release()
        cv2.destroyAllWindows()