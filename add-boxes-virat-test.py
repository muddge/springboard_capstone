import os, glob, re
import cv2
import pandas as pd
import warnings
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/test-file'
files = os.listdir(path)

for f in files:

    if f.endswith('.mp4'):

        filename = re.search(r'^(.+)\.mp4', f).group(1)
        saved_filename = filename + '-out.mp4'
        objects_data_file = filename + '.viratdata.objects.txt'

        objects_df = pd.read_csv(path + r'/' + objects_data_file, header=None, sep=' ', \
                                 names=['id','dur','frame','left_top_x','left_top_y','width','height','type'], \
                                 usecols=['id','frame','left_top_x','left_top_y','width','height','type'])

        person_df = objects_df[objects_df['type'] == 1]

        cap = cv2.VideoCapture(path + r'/' + f)
        fps = cap.get(cv2.CAP_PROP_FPS)

        out = cv2.VideoWriter(path + r'/' + saved_filename, cv2.VideoWriter_fourcc(*'MP4V'), \
                                  fps, (int(cap.get(3)), int(cap.get(4))))

        if (cap.isOpened() == False):
            print("Error opening video file " + f)

        while (cap.isOpened()):

            ret, frame = cap.read()

            # Capture frame by frame, write circle to upper left corner of frame
            if (ret == True):

                current_frame_number = cap.get(1)
                persons_in_current_frame_df = person_df[person_df['frame'] == current_frame_number]

                if (persons_in_current_frame_df.empty):

                    out.write(frame)

                else:

                    for index, row in persons_in_current_frame_df.iterrows():

                        bbox_top_left_x = row['left_top_x']
                        bbox_top_left_y = row['left_top_y']
                        width = row['width']
                        height = row['height']

                        #print(frame, ' ', bbox_top_left_x, ' ', bbox_top_left_y, ' ', width, ' ', height)

                        start_point = (bbox_top_left_x, bbox_top_left_y)
                        end_point = (bbox_top_left_x + width, bbox_top_left_y + height)
                        color = (0, 255, 0)
                        thickness = 2

                        cv2.rectangle(frame, start_point, end_point, color, thickness)

                    out.write(frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

        # Release VideoCapture object
        cap.release()
        out.release()

        # Closes all frames
        cv2.destroyAllWindows()
