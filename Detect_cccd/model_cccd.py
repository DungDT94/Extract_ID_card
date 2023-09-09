from ultralytics import YOLO
import numpy as np
import cv2
import torch.nn as nn
from config import weight_cccd
from Detect_cccd.padding import padding_image


class DetectCCCD(nn.Module):
    def __init__(self, use_gpu):
        if use_gpu:
            self.device = 0
        else:
            self.device = 'cpu'
        self.model = YOLO(weight_cccd)

    def predict(self, image_pil):
        result = self.model(source=image_pil, show=False, device = self.device)
        boxes = result[0].boxes
        list_box = []
        for box in boxes:
            box2list = box.xyxy.tolist()
            box2list = np.reshape(box2list, (4,))
            box2list = box2list.tolist()
            list_box.append(box2list)
        width, height = image_pil.size
        list_anh_cccd = []
        if len(list_box) != 0:
            for box in list_box:
                crop = image_pil.crop((box[0] - int(width/20), box[1] - int(height/20), box[2] + int(width/20), box[3] + int(height/20)))
                crop_pad_pil = padding_image(crop)
                crop_pad_cv2 = cv2.cvtColor(np.array(crop_pad_pil), cv2.COLOR_RGB2BGR)
                list_anh_cccd.append(crop_pad_cv2)
            return list_anh_cccd
        else:
            return None





