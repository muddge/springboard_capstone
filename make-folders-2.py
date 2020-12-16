import os

save_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/transfer-learning/data/ground-truth'
video_path = '/Users/jason/Desktop/springboard/capstone-datasets/VIRAT/virat-ground'

files = [f for f in os.listdir(video_path) if f.endswith('.mp4')]

for f in files:

    os.mkdir(os.path.join(save_path,f.split('.')[0]))