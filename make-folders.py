import cv2, os
import pandas as pd
import numpy as np

save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/transfer-learning/data/images'
video_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground'

files = [f for f in os.listdir(video_path) if f.endswith('.mp4')]

for f in files:

    os.mkdir(os.path.join(save_path,f.split('.')[0]))