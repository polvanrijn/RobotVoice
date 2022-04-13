import json
from os.path import exists, basename, join
import cv2
import tempfile
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from shutil import move


def read_json(file_path):
    assert exists(file_path)
    with open(file_path, 'r') as f:
        contents = json.load(f)
    return contents

def save_json(obj, file_path):
    with open(file_path, 'w') as f:
        json.dump(obj, f)


def pad_images_to_same_size(images):
    """
    :param images: sequence of images
    :return: list of images padded so that all images have same width and height (max width and height are used)
    """
    width_max = 0
    height_max = 0
    for img in images:
        h, w = img.shape[:2]
        width_max = max(width_max, w)
        height_max = max(height_max, h)

    images_padded = []
    for img in images:
        h, w = img.shape[:2]
        diff_vert = height_max - h
        pad_top = diff_vert//2
        pad_bottom = diff_vert - pad_top
        diff_hori = width_max - w
        pad_left = diff_hori//2
        pad_right = diff_hori - pad_left
        img_padded = cv2.copyMakeBorder(img, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=0)
        assert img_padded.shape[:2] == (height_max, width_max)
        images_padded.append(img_padded)

    return images_padded

input_json = 'robots.json'
output_json = 'processed_robots.json'
robots = read_json(input_json)

processed_robots = read_json(output_json) if exists(output_json) else {}

for robot in robots:
    photos = robot['photos']
    n_pics = len(photos)
    bot_name = robot['name']

    if bot_name in processed_robots.keys():
        continue

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Download images
        imgs = []
        urls = []
        for idx, url in enumerate(photos):
            # Fixes a minor bug in the scraping script
            high_res_url = url if idx == 0 else url.replace('-thumb@2x', '-full').replace('/HD/', '/SD/')
            urls.append(high_res_url)
            subprocess.call(f'cd {tmp_dir}; wget {high_res_url}', shell=True)
            imgs.append(cv2.imread(join(tmp_dir, basename(high_res_url))))

        image_array = np.concatenate(pad_images_to_same_size(imgs), axis=1)



        valid_response = False
        while not valid_response:
            fig = figure(figsize=(30, 6), dpi=80)
            plt.imshow(image_array)
            plt.axis('off')
            plt.show(block=False)

            response = input(f'Do you want to add "{bot_name}"? N/<1-{n_pics}>')
            plt.close(fig)
            print(response)

            if response in ['N', 'n']:
                valid_response = True
            try:
                int_response = int(response)
                if int_response > 0 and int_response <= n_pics:
                    # Update processed_robots
                    valid_response = True
                    robot['photo'] = urls[int_response-1]
                    processed_robots[bot_name] = robot

                    # move image to images
                    photo_name = basename(robot['photo'])
                    move(join(tmp_dir, photo_name), join('images', photo_name))

                    save_json(processed_robots, output_json)
            except:
                pass


