import os, glob, re, time
import cv2
import csv
import numpy as np
import torch
from torch import nn
import argparse
from sys import platform

from models import *
from utils.datasets import *
from utils.utils import *

from IPython.display import HTML
from base64 import b64encode

path1 = '/content/drive/My Drive/VIRAT/virat-aerial/'
path2 = '/content/drive/My Drive/VIRAT/virat-ground/'
path3 = '/content/drive/My Drive/3dpes/'

#files_path1 = os.listdir(path1)
files_path2 = os.listdir(path2)
files_path3 = os.listdir(path3)

print(torch.cuda.device_count())
#for f in files_path2:
 # print(f)

parser = argparse.ArgumentParser()
parser.add_argument('--cfg', type=str, default='cfg/yolov3.cfg', help='*.cfg path')
parser.add_argument('--names', type=str, default='data/coco.names', help='*.names path')
parser.add_argument('--weights', type=str, default='weights/yolov3.pt', help='weights path')
parser.add_argument('--img-size', type=int, default=416, help='inference size (pixels)')
parser.add_argument('--conf-thres', type=float, default=0.3, help='object confidence threshold')
parser.add_argument('--iou-thres', type=float, default=0.6, help='IOU threshold for NMS')
parser.add_argument('--device', default='', help='device id (i.e. 0 or 0,1) or cpu')
parser.add_argument('--classes', nargs='+', type=int, help='filter by class')
parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
opt = parser.parse_args(args = [])

weights = opt.weights
img_size =  opt.img_size

# Initialize Device
device = torch_utils.select_device(opt.device)

# Initialize model
model = Darknet(opt.cfg, img_size)

# Load weights
attempt_download(weights)
if weights.endswith('.pt'):  # pytorch format
    model.load_state_dict(torch.load(weights, map_location=device)['model'])
else:  # darknet format
    load_darknet_weights(model, weights)

model.to(device).eval();
# Get names and colors
names = load_classes(opt.names)
colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]
print(names)

%cd ..

def predict_one_video(path_video):

    videoname = os.path.split(path_video)[-1]

    output_dir = '/content/drive/My Drive/VIRAT/virat-ground/output'
    resultsfile = output_dir + '/' + videoname + '.predictions.csv'

    with open(resultsfile, 'w') as csvfile:

        csvwriter = csv.writer(csvfile, delimiter = ' ')

        #print("Calling predict_one_video function on: " + path_video)
        cap  = cv2.VideoCapture(path_video)
        _, img0 = cap.read()

        save_path = os.path.join(output_dir, videoname)
        fps = cap.get(cv2.CAP_PROP_FPS) # video frames per second
        w = int(cap.get(3)) # video pixel width
        h = int(cap.get(4)) # video pixel height
        out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h)) # object to save video output

        while img0 is not None:

            # Padded resize
            img = letterbox(img0, new_shape=opt.img_size)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3xHxW
            img = np.ascontiguousarray(img)

            img = torch.from_numpy(img).to(device)
            img = img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            pred = model(img)[0]
            # Apply NMS
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                im0 = img0 ##### Ganti im0s menjadi img0

                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Write results
                    for *xyxy, conf, cls in det:
                        label = '%s %.2f' % (names[int(cls)], conf)
                        if label.startswith('person'):
                            frame = int(cap.get(1)) # get frame number
                            a = label.split(' ')[0] # string 'person'
                            b = label.split(' ')[1] # class confidence of prediction
                            c = str(xyxy[0].data.tolist()).strip('.')[:-2] # bounding box coordinate
                            d = str(xyxy[1].data.tolist()).strip('.')[:-2] # bounding box coordinate
                            e = str(xyxy[2].data.tolist()).strip('.')[:-2] # bounding box coordinate
                            f = str(xyxy[3].data.tolist()).strip('.')[:-2] # bounding box coordinate
                            objectrow = [frame,a,b,c,d,e,f] # list of above
                            #print(*objectrow, sep=' ')
                            csvwriter.writerow(objectrow)
                            plot_one_box(xyxy, im0, label=label, color=colors[int(cls)])

            out.write(im0)
            _, img0 = cap.read()
            print("Saving video: " + path_video)

        out.release()

        return save_path

#for i in range(2, len(files_path1)):

    #path_video = os.path.join(files_path1[i])
    #path_video = path1 + path_video
    #save_path = predict_one_video(path_video)


for f in files_path2:

    path_video = os.path.join(f)
    path_video = path2 + path_video
    save_path = predict_one_video(path_video)
