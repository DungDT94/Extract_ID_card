def box_coordinate(dict_info_key):
    lst_all = []
    for bndbox in dict_info_key:
        lst_temp = []
        for i in range(4):
            lst_temp.append(int(bndbox[i]))
        lst_all.append(lst_temp)
    return lst_all


def calculate_iou(boxA, boxB):
    x_min = max(float(boxA[0]), float(boxB[0]))
    y_min = max(float(boxA[1]), float(boxB[1]))
    x_max = min(float(boxA[2]), float(boxB[2]))
    y_max = min(float(boxA[3]), float(boxB[3]))
    intersection_area = max((x_max - x_min), 0)*max((y_max - y_min), 0)
    boxA_area = (float(boxA[2]) - float(boxA[0])) * (float(boxA[3]) - float(boxA[1]))
    boxB_area = (float(boxB[2]) - float(boxB[0])) * (float(boxB[3]) - float(boxB[1]))
    area_union = boxA_area + boxB_area - intersection_area
    iou = intersection_area / area_union
    return iou


def remove_duplicate(list_box):
    list_trung = []
    list_box_final = []
    if len(list_box) == 1:
        return list_box
    else:
        for i in range(len(list_box)-1):
            for j in range(i+1, len(list_box)):
                #print(list_box[i])
                #print(list_box[j])
                iou = calculate_iou(list_box[i], list_box[j])
                #print(iou)
                if iou > 0.88:
                    list_trung.append(j)
                continue
        list_trung = list(set(list_trung))
        for i in range(len(list_box)):
            if i not in list_trung:
                list_box_final.append(list_box[i])
        return list_box_final   


def check_iou_y(box_a, box_b):
    ymin = max(float(box_a[1]), float(box_b[1]))
    ymax = min(float(box_a[3]), float(box_b[3]))
    minus = min(float(box_a[3]) - float(box_a[1]), float(box_b[3]) - float(box_b[1]))
    iou = (ymax - ymin) / minus
    #print(iou)
    if iou > 0.17:
        return True
    else:
        return False


def sort_same_line(list_box):
    list_box = remove_duplicate(list_box)
    box_index = []
    list_box_final = []
    if len(list_box) == 1:
        list_box_final.append(list_box)
    else:
        for i in range(len(list_box)-1):
            list_temp = []
            if i in box_index:
                continue
            else:
                list_temp.append(list_box[i])
                for j in range(i+1, len(list_box)):
                    if j in box_index:
                        continue
                    else:
                        #print(check_iou_y(list_box[i], list_box[j]))
                        if check_iou_y(list_box[i], list_box[j]):
                            list_temp.append(list_box[j])
                            box_index.append(j)
                list_temp.sort(key=lambda x: x[0])
                list_box_final.append(list_temp)

    list_box_sort_final = []
    list_y_min = []
    for line in list_box_final:
        ymin_box = [box[1] for box in line]
        list_y_min.append(min(ymin_box))
    list_y_min_sort = sorted(list_y_min)
    for ymin in list_y_min_sort:
        index = list_y_min.index(ymin)
        list_box_sort_final.append(list_box_final[index])
    return list_box_sort_final    




