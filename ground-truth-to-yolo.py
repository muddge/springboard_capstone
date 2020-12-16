import os, csv
import numpy as np
import pandas as pd


path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/annotations'
save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/ground-truth-in-yolo-format'

width_height_data = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground-width-height/virat-ground-height-width.csv'
width_height_df = pd.read_csv(width_height_data, sep=' ', header=0, names=['file', 'width', 'height'], index_col='file')

files_path = os.listdir(path)

files_path = [f for f in files_path if f.endswith('objects.txt')]


for f in files_path:

    filename = path + '/' + f

    saved_filename = save_path + '/' + f.split('.')[0] + '.txt'

    try:

        results_df = pd.read_csv(filename, sep=' ', header=0, names=['id', 'duration', 'frame', 'top_left_x',
                                                                 'top_left_y', 'box_width', 'box_height', 'type'])

    except:

        print(f)

    results_df = results_df[results_df['type'] == 1]

    results_df['person'] = 0

    try:

        video_width = width_height_df.at[f, 'width']

        video_height = width_height_df.at[f, 'height']

    except:

        continue

    results_df['x_center'] = np.floor(results_df['top_left_x'] + (results_df['box_width'] / 2))

    results_df['y_center'] = np.floor(results_df['top_left_y'] + (results_df['box_height'] / 2))

    results_df['x_center'] = results_df['x_center'] / video_width

    results_df['y_center'] = results_df['y_center'] / video_height

    results_df['box_width'] = results_df['box_width'] / video_width

    results_df['box_height'] = results_df['box_height'] / video_width

    results_df = results_df[['person', 'x_center', 'y_center', 'box_width', 'box_height', 'frame']]

    results_df.to_csv(saved_filename, header=False, sep=' ', index=False, quoting=csv.QUOTE_NONE)