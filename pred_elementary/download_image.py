import requests
import argparse


def download_image(image_url, image_name):
    img_data = requests.get(image_url).content
    with open(image_name, 'wb') as handler:
        handler.write(img_data)


if __name__ == '__main__':
    a = argparse.ArgumentParser()
    a.add_argument("--imageUrl", help="image url", required=True)
    a.add_argument("--imageName", help="image name", required=True)
    args = a.parse_args()
    download_image(args.imageUrl, args.imageName)
