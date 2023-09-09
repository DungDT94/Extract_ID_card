from Detect_cccd.model_cccd import *
from Detect_goc.model_corner import DetectCorner
from OCR.load_ocr import *
from Detect_info.detect_info import DetectInfo
from PIL import Image
from sort import *
import json


class Extract:
    def __init__(self):
        self.use_gpu = True
        self.model_ocr = OCR(self.use_gpu)
        self.detect_cccd = DetectCCCD(self.use_gpu)
        self.detect_corner = DetectCorner(self.use_gpu)
        self.detect_info = DetectInfo(self.model_ocr, self.use_gpu, 7)

    def predict(self, image_p):
        lst_cccd = self.detect_cccd.predict(image_p)
        lst_img_warped = self.detect_corner.predict(lst_cccd)
        lst_dict_info = {}
        i = 0
        if lst_img_warped is not None:
            for img_warped in lst_img_warped:
                img_warped_crop = cv2.cvtColor(img_warped, cv2.COLOR_BGR2RGB)
                pil_warped = Image.fromarray(img_warped_crop)
                dict_info = self.detect_info.pred(img_warped)
                if len(dict_info) != 0:
                    for key in dict_info:
                        label_all = ''
                        dict_info[key] = sort_same_line(dict_info[key])
                        for box_line in dict_info[key]:
                            for subbox in box_line:
                                image_crop = pil_warped.crop((subbox[0], subbox[1], subbox[2], subbox[3]))
                                image_results, label = self.model_ocr.predict(image_crop)
                                label_all += ' ' + label
                        label_all = label_all.strip()
                        dict_info[key] = label_all
                    lst_dict_info.update(dict_info)
        lst_dict_info = json.dumps(lst_dict_info)
        lst_dict_info = json.loads(lst_dict_info)
        return lst_dict_info, lst_img_warped


