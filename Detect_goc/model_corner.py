from Detect_cccd.model_cccd import *
from config import weight_goc
from Detect_goc.image_process import *


class DetectCorner(nn.Module):
    def __init__(self, use_gpu):
        super().__init__()
        if use_gpu:
            self.device = 0
        else:
            self.device = 'cpu'
        self.model = YOLO(weight_goc)

    def predict(self, lst_cccd):
        lst_img_warped = []
        if lst_cccd is not None:
            for img in lst_cccd:
                result = self.model(source=img, show=False, save=False, device = self.device)
                boxes = result[0].boxes
                list_box = []
                dict_point = {}
                keys = []
                for box in boxes:
                    label = int(box.cls.tolist()[0])
                    score = float(box.conf.tolist()[0])
                    box2list = box.xyxy.tolist()
                    box2list = np.reshape(box2list, (4,))
                    box2list = box2list.tolist()
                    dict_point[label] = box2list
                    keys.append(label)
                    list_box.append(dict_point[label])
                lst_box_center = get_center_point(list_box)
                for i in range(len(lst_box_center)):
                    dict_point[keys[i]] = lst_box_center[i]
                list_box_final = []
                if len(dict_point) == 4:
                    list_box_final.extend([dict_point[0], dict_point[1], dict_point[2], dict_point[3]])
                    pts = np.array(list_box_final, dtype="float32")
                    warped = four_point_transform_2(img, pts)
                elif len(dict_point) == 3:
                    list_box_final = detect_3(dict_point)
                    pts = np.array(list_box_final, dtype="float32")
                    warped = four_point_transform_2(img, pts)
                else:
                    warped = detect_1(dict_point, img)
                lst_img_warped.append(warped)
        else:
            return None
        return lst_img_warped


