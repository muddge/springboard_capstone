import os, csv

path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-annotations-v2/annotations'

files_path = os.listdir(path)

for f in files_path:

    if f.endswith('objects.txt'):

        saved_filename = path + '/' + f.split('.')[0] + '.ground-truth.csv'

        with open(path + '/' + f, newline='') as csvfile:

            reader = csv.reader(csvfile, delimiter=' ')

            with open(saved_filename, 'w') as resultscsv:

                writer = csv.writer(resultscsv, delimiter = ' ')

                object_dict = {
                    '':'n/a',
                    '0':'n/a',
                    '1':'person',
                    '2':'car',
                    '3':'vehicle',
                    '4':'object',
                    '5':'bike'
                }

                for row in reader:

                    object_type = object_dict[row[-1]]
                    frame = int(row[2])
                    left = int(row[3])
                    top = int(row[4])
                    right = left + int(row[5])
                    bottom = top + int(row[6])
                    if object_type != 'person':
                        newrow = [object_type, left, top, right, bottom, 'difficult']
                    else:
                        newrow = [object_type, left, top, right, bottom]
                    writer.writerow(newrow)

