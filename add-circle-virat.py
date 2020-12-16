import os, glob, re, csv
import cv2
import numpy as np

path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/test-file'
files = os.listdir(path)

for f in files:

    if f.endswith('.mp4'):

        filename = re.search(r'^(.+)\.mp4', f).group(1)
        saved_filename = filename + '-out.mp4'
        objects_data_file = filename + '.viratdata.objects.txt'

        with open(path + r'/' + objects_data_file) as objects_file:

            objectreader = csv.reader(objects_file, delimiter=' ')
            person_rows = [row for row in objectreader if row[7] == '1']

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
                    persons_in_current_frame = [row for row in person_rows if int(row[2]) == current_frame_number]

                    if not persons_in_current_frame:

                        out.write(frame)

                    else:

                        for row in persons_in_current_frame:
                            bbox_top_left_x = int(row[3])
                            bbox_top_left_y = int(row[4])
                            width = int(row[5])
                            height = int(row[6])

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
