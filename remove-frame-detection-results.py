import csv, os

path = '/Users/jason/Desktop/springboard/virat-ground-pre-trained-detection-results'

save_path = '/Users/jason/Desktop/springboard/virat-ground-pre-trained-detection-results/revised'

files_path = os.listdir(path)

for f in files_path:

    if f.endswith('csv'):

        saved_filename = save_path + '/' + f.split('.')[0] + '.txt'

        with open(path + '/' + f, encoding='utf8', errors='ignore') as reader:

            with open(saved_filename, 'w') as resultscsv:

                writer = csv.writer(resultscsv, delimiter=' ')

                for row in reader:

                    newrow = row.split(' ')[1:]
                    for str in newrow:
                        str.strip('"')
                    writer.writerow(newrow)