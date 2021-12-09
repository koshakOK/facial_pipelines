import pandas as pd
import cv2
import os
import argparse
from misc import download_image


def is_valid(raw_index, df):
    kp = df.loc[raw_index, ["OUTPUT:image"]].values[0]
    arr_kp = kp.split('{')[1:]
    if len(arr_kp) != 68:
        return False
    time = int(df.loc[raw_index, ["ASSIGNMENT:time_spent"]].values)
    if time < 20:
        return False
    return True


def get_key_points(path_to_csv, path_to_images, max_number):
    image_names = []
    df = pd.read_csv(path_to_csv, sep=';')
    kps = []
    for i in range(100, int(max_number), 10):
        kp = df.loc[i, ["OUTPUT:image"]].values[0]
        if not is_valid(i, df):
            continue
        arr_kp = kp.split('{')[1:]

        url = df.loc[i, ["INPUT:image"]].values[0]

        # download image
        name = "image" + str(i) + ".jpg"
        result_path = os.path.join(path_to_images, name)
        image_names.append(result_path)
        download_image(url, result_path)

        # get key points
        temp = []
        for i in arr_kp:
            temp.append(i.split(","))
        x = []
        y = []
        for i in temp:
            x.append(float(i[1][7:]))
            y.append(float(i[2][6:]))
        kps.append((x[48:68], y[48:68]))

    return kps, image_names


def save_result_image(kps, image_path, result_path):
    cv_keypoints = []
    for i in range(20):
        cv_keypoints.append(cv2.KeyPoint(kps[0][i], kp[1][i], 5.))
    img = cv2.imread(image_path)
    resultimage = cv2.drawKeypoints(img, cv_keypoints, 0, (0, 255, 0))
    cv2.imwrite(result_path, resultimage)


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument("--path_to_csv",
                   help="path to cvs file from Elementary ABC",
                   required=True)
    a.add_argument("--path_to_images",
                   help="path where to store downloaded images",
                   required=True)
    a.add_argument("--max_number",
                   help="max number of raws",
                   required=True)
    a.add_argument("--path_to_results",
                   help="path where to store result images",
                   required=True)
    args = a.parse_args()
    kps, image_names = get_key_points(args.path_to_csv,
                                      args.path_to_images,
                                      args.max_number)
    for i in range(len(image_names)):
        kp = kps[i]
        image_name = image_names[i]
        name = "result" + image_name[11:]
        result_path = os.path.join(args.path_to_results, name)
        save_result_image(kp, image_name, result_path)
