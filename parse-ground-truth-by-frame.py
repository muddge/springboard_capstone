import os,csv
import pandas as pd

load_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/ground-truth-in-yolo-format'
save_path_root = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/transfer-learning/data/ground-truth'

files = os.listdir(load_path)

for f in files:

    filename = f.split('.')[0]

    frames_df = pd.read_csv(load_path + '/' + f, sep=' ', header=0, names=['class', 'x-center', 'y-center', 'width',
                                                                           'height', 'frame'])

    frames_list = frames_df['frame'].tolist()

    for frame in frames_list:

        frame_sub_df = frames_df[frames_df['frame'] == frame]
        frame_sub_df.drop('frame', axis=1, inplace=True)
        saved_file = os.path.join(save_path_root, filename, filename + '-' + str(frame) + '.txt')
        frame_sub_df.to_csv(saved_file, header=False, sep=' ', index=False, quoting=csv.QUOTE_NONE)