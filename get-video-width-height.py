import os, csv
import numpy as np
import pandas as pd
import cv2

path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground'
save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground-width-height'

files = [f for f in os.listdir(path) if f.endswith('.mp4')]

saved_filename = save_path + '/virat-ground-height-width.csv'

with open(saved_filename, 'w') as resultscsv:

    writer = csv.writer(resultscsv, delimiter=' ')

    for f in files:

        try:
            cap = cv2.VideoCapture(path + r'/' + f)
        except:
            print(f)
        name = f.split('.')[0] + '.viratdata.objects.txt'
        width= int(cap.get(3)) # get video width pixels
        height = int(cap.get(4)) # get video height in pixels
        row = [name, width, height]
        writer.writerow(row)