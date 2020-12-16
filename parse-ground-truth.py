import os, csv
import pandas as pd

path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/annotations'

save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/ground-truth-frame-number'

files_path = os.listdir(path)

sublist = ['VIRAT_S_010003_00_000000_000108.viratdata.objects.txt',
           'VIRAT_S_000205_01_000197_000342.viratdata.objects.txt',
           'VIRAT_S_000200_06_001693_001824.viratdata.objects.txt']

intersection = [f for f in files_path if f in sublist]

for f in intersection:

    filename = path + '/' + f

    results_df = pd.read_csv(filename, sep=' ', header=0, names=['id', 'duration', 'frame', 'left',
                                                                 'top', 'width', 'height', 'type'])

    frame_list = results_df['frame'].unique().tolist()

    for frame in frame_list:
        saved_filename = save_path + '/' + f.split('.')[0] + '-' + str(frame) + '.txt'
        subresults_df = results_df[results_df['frame'] == frame]
        subresults_df = subresults_df[subresults_df['type'] == 1]
        subresults_df['person'] = 'person'
        subresults_df.drop(['frame'], axis=1, inplace=True)
        subresults_df['right'] = subresults_df['left'] + subresults_df['width']
        subresults_df['bottom'] = subresults_df['top'] + subresults_df['height']
        cols = list(subresults_df.columns.values)
        subresults_df = subresults_df[['person', 'left', 'top', 'right', 'bottom']]
        if subresults_df is not None:
            subresults_df.to_csv(saved_filename, header=False, sep=' ', index=False, quoting=csv.QUOTE_NONE)