import os, csv
import pandas as pd

path = '/Users/jason/Desktop/springboard/virat-ground-pre-trained-detection-results'

save_path = '/Users/jason/Desktop/springboard/virat-ground-pre-trained-detection-results/revised-frame-number'

files_path = os.listdir(path)

for f in files_path:

    counter = 0
    while counter < 3:

        if f.endswith('csv'):

            filename = path + '/' + f

            results_df = pd.read_csv(filename, sep= ' ', header=0, names=['A','B','C','D','E','F','G'])

            frame_list = results_df['A'] .tolist()

            for frame in frame_list:
                saved_filename = save_path + '/' + f.split('.')[0] + '-' + str(frame) + '.txt'
                subresults_df = results_df[results_df['A'] == frame]
                subresults_df.drop(['A'], axis=1, inplace=True)
                if subresults_df is not None:
                    subresults_df.to_csv(saved_filename, header=False, sep=' ', index=False, quoting=csv.QUOTE_NONE)

            counter = counter + 1
        #results_df.drop(['A'], axis=1, inplace=True)

        #results_df.to_csv(saved_filename, header=False, sep=' ', index=False, quoting=csv.QUOTE_NONE)