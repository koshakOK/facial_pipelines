import argparse
import cv2
import os


def extractImages(path_to_video_folder, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(path_to_video_folder)
    success, image = vidcap.read()
    success = True
    os.mkdir(pathOut)
    name_of_video = pathOut.split('/')[1]
    while success:
        cv2.imwrite(pathOut + name_of_video + "_frame%d.jpg" % count, image)
        success, image = vidcap.read()
        count += 1


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--pathIn", help="path to video")
    args = a.parse_args()

    videos = []
    with os.scandir(args.pathIn) as it:
        for entry in it:
            pathOut = args.pathIn + "/" + entry.name.split('.')[0] + '/'
            videos.append((entry.path, pathOut))
    for video in videos:
        extractImages(video[0], video[1])
