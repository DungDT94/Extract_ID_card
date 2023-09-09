from CenterNet.detectors.base_detector import *
import torch.nn as nn
from config import weight_info


class DetectInfo(nn.Module):
    def __init__(self, model_ocr, use_gpu, num_classes):
        super().__init__()
        self.vis_thresh = 0.3
        self.num_classes = num_classes
        self.detector = BaseDetector(weight_info, self.num_classes, use_gpu)

    def pred(self, img_warped):
        if img_warped is None:
            return None
        else:
            ret = self.detector.run(img_warped)['results']
            lst_all = []
            for label in range(1, self.num_classes + 1):
                lst = []
                for bbox in ret[label]:
                    lst_temp = []
                    if bbox[4] > self.vis_thresh:
                        lst_temp.extend([bbox[0], bbox[1], bbox[2], bbox[3]])
                    if len(lst_temp) != 0:
                        lst.append(lst_temp)
                lst_all.append(lst)
            dict_key = ['id', 'name', 'date','sex', 'nationality', 'add', 'residence' ]
            dict_info = {}
            for i in range(len(lst_all)):
                dict_info[dict_key[i]] = lst_all[i]
            return dict_info


