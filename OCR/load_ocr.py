import os
import glob
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import torch.nn as nn
import cv2
import uuid
from PIL import Image
import time

class OCR(nn.Module):
    def __init__(self, use_gpu):
        if use_gpu:
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        super().__init__()
        self.config = Cfg.load_config_from_name('vgg_transformer')
        self.config['device'] = self.device
        self.config['cnn']['pretrained'] = False
        self.config['predictor']['beamsearch'] = False
        self.detector = Predictor(self.config)

    def predict(self, img):
        img = img
        result = self.detector.predict(img)
        return img, result





