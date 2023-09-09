import numpy as np
import cv2

def get_center_point(coordinate_lst):
    lst = []
    for box in coordinate_lst:
        x_center = (float(box[0]) + float(box[2])) / 2
        y_center = (float(box[1]) + float(box[3])) / 2
        lst.append((x_center, y_center))
    return lst


def four_point_transform_2(image, rect):
    (tl, tr, br, bl) = rect
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (max_width, max_height))
    return warped


def detect_3(dict_point):
    if len(dict_point) == 3:
        temp_x = 0
        temp_y = 0
        if 0 not in dict_point:
            cross_x = abs(dict_point[3][0] - dict_point[1][0])
            cross_y = abs(dict_point[3][1] - dict_point[1][1])
            if dict_point[2][0] > cross_x:
                temp_x = dict_point[2][0] - cross_x
            elif dict_point[2][0] < cross_x:
                temp_x = cross_x + dict_point[2][0]
            if dict_point[2][1] > cross_y:
                temp_y = dict_point[2][1] - cross_y
            elif dict_point[2][1] < cross_y:
                temp_y = dict_point[2][1] + cross_y
            dict_point[0] = (temp_x, temp_y)
        elif 1 not in dict_point:
            cross_x = abs(dict_point[2][0] - dict_point[0][0])
            cross_y = abs(dict_point[2][1] - dict_point[0][1])
            if dict_point[3][0] > cross_x:
                temp_x = dict_point[3][0] - cross_x
            elif dict_point[3][0] < cross_x:
                temp_x = cross_x + dict_point[3][0]
            if dict_point[3][1] > cross_y:
                temp_y = dict_point[3][1] - cross_y
            elif dict_point[3][1] < cross_y:
                temp_y = dict_point[3][1] + cross_y
            dict_point[1] = (temp_x, temp_y)
        elif 2 not in dict_point:
            cross_x = abs(dict_point[3][0] - dict_point[1][0])
            cross_y = abs(dict_point[3][1] - dict_point[1][1])
            if dict_point[0][0] > cross_x:
                temp_x = dict_point[1][0] - cross_x
            elif dict_point[0][0] < cross_x:
                temp_x = cross_x + dict_point[1][0]
            if dict_point[0][1] > cross_y:
                temp_y = dict_point[0][1] - cross_y
            elif dict_point[0][1] < cross_y:
                temp_y = dict_point[0][1] + cross_y
            dict_point[2] = (temp_x, temp_y)
        elif 3 not in dict_point:
            cross_x = abs(dict_point[2][0] - dict_point[0][0])
            cross_y = abs(dict_point[2][1] - dict_point[0][1])
            if dict_point[1][0] > cross_x:
                temp_x = dict_point[1][0] - cross_x
            elif dict_point[1][0] < cross_x:
                temp_x = cross_x + dict_point[1][0]
            if dict_point[1][1] < cross_y:
                temp_y = dict_point[1][1] - cross_y
            elif dict_point[1][1] < cross_y:
                temp_y = dict_point[1][1] + cross_y
            dict_point[3] = (temp_x, temp_y)
    list_box_final = [dict_point[0], dict_point[1.0], dict_point[2], dict_point[3]]
    return list_box_final


def detect_1(dict_point, image):
    height = image.shape[0]
    width = image.shape[1]
    if 0 in dict_point:
        coor = dict_point[0]
        if int(coor[1]) in range(int(height/2) + 1) and int(coor[0]) in range(int(width/2), width + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif int(coor[1]) in range(int(height / 2) + 1) and int(coor[0]) in range(int(width / 2) + 1):
            pass
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2), width + 1):
            image = cv2.rotate(image, cv2.ROTATE_180)
    elif 1 in dict_point:
        coor = dict_point[1]
        if int(coor[1]) in range(int(height/2) + 1) and int(coor[0]) in range(int(width/2), width + 1):
            pass
        elif int(coor[1]) in range(int(height / 2) + 1) and int(coor[0]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2), width + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif 2 in dict_point:
        coor = dict_point[2]
        if int(coor[1]) in range(int(height/2) + 1) and int(coor[0]) in range(int(width/2), width + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif int(coor[1]) in range(int(height / 2) + 1) and int(coor[0]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[0]) in range(int(width / 2), width + 1):
            pass
    elif 3 in dict_point:
        coor = dict_point[3]
        if int(coor[1]) in range(int(height/2) + 1) and int(coor[1]) in range(int(width/2), width + 1):
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif int(coor[1]) in range(int(height / 2) + 1) and int(coor[1]) in range(int(width / 2) + 1):
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[1]) in range(int(width / 2) + 1):
            pass
        elif int(coor[1]) in range(int(height/2),  height+1) and int(coor[1]) in range(int(width / 2), width + 1):
            print(4)
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return image