import os
import time
import numpy as np
from PIL import Image
from skimage import util
from skimage import filters
import cv2
import argparse


parser = argparse.ArgumentParser(description='Starting Image distortion generator')
parser.add_argument('-load_image_directory', default='./dataset/', type=str)
parser.add_argument('-directory_to_save_to', default='./distorted_dataset/', type=str)

args, _ = parser.parse_known_args()

if not os.path.isdir(args.load_image_directory):
    print(f'folder {args.load_image_directory} does not exist! '
          f'please provide existing folder in -load_image_directory arg!')
    exit()

if not os.path.isdir(args.directory_to_save_to):
    print(f'folder {args.directory_to_save_to} does not exist! '
          f'please provide existing folder in -directory_to_save_to arg!')
    exit()

print(f"Directory to retrieve the images: {args.load_image_directory}")
print(f"Directory to store new images: {args.directory_to_save_to}")

dataset_dir = args.load_image_directory
# may need to save in separate directories specific to the distortion applied
#distorted_dataset_dir = "./distorted_dataset/"
distorted_dataset_dir = args.directory_to_save_to


# add various noise to an image with a specified variance
def add_noise(img, noise_mode):
    applied_noise_1 = None
    applied_noise_2 = None
    applied_noise_3 = None
    if noise_mode == "gaussian":
        # variance = rand(1,100)
        applied_noise_1 = util.random_noise(img, mode=noise_mode, clip=True, var=0.0125)
        time.sleep(0.02)
        applied_noise_2 = util.random_noise(img, mode=noise_mode, clip=True, var=0.025)
        time.sleep(0.02)
        applied_noise_3 = util.random_noise(img, mode=noise_mode, clip=True, var=0.00)
        time.sleep(0.02)
    elif noise_mode == "s&p":
        applied_noise_1 = util.random_noise(img, mode=noise_mode, clip=True, salt_vs_pepper=0.0125)
        time.sleep(0.02)
        applied_noise_2 = util.random_noise(img, mode=noise_mode, clip=True, salt_vs_pepper=0.025)
        time.sleep(0.02)
        applied_noise_3 = util.random_noise(img, mode=noise_mode, clip=True, salt_vs_pepper=0.05)
        time.sleep(0.02)
    elif noise_mode == "speckle":
        applied_noise_1 = util.random_noise(img, mode=noise_mode, clip=True, var=0.0125)
        time.sleep(0.02)
        applied_noise_2 = util.random_noise(img, mode=noise_mode, clip=True, var=0.025)
        time.sleep(0.02)
        applied_noise_3 = util.random_noise(img, mode=noise_mode, clip=True, var=0.05)
        time.sleep(0.02)
    return applied_noise_1, applied_noise_2, applied_noise_3


# gaussian blur with sigma variation
def gaussian_blur_noise(image):
    g_image1 = filters.gaussian(image, sigma=1.5, multichannel=False)
    g_image2 = filters.gaussian(image, sigma=3, multichannel=False)
    g_image3 = filters.gaussian(image, sigma=6, multichannel=False)
    return g_image1, g_image2, g_image3


# apply noise calls apply noise above
def distort_and_save_images(image_from_dataset, name):

    # gaussian blur
    gb_1, gb_2, gb_3 = gaussian_blur_noise(image_from_dataset)
    # gaussian noise
    gn_1, gn_2, gn_3 = add_noise(image_from_dataset, "gaussian")
    # salt and pepper noise
    sp_1, sp_2, sp_3 = add_noise(image_from_dataset, "s&p")
    # speckle noise
    s_1, s_2, s_3 = add_noise(image_from_dataset, "speckle")

    # apply_noise returns a floating-point image in the range
    # [0, 1] so we need to change it to 'uint8' with range [0,255]
    gb1, gb2, gb3 = convert_to_unit8(gb_1, gb_2, gb_3)
    # gaussian blur prefix and pathing
    gb_prefix = "_gaussian_blur"
    gb_path_to_save = distorted_dataset_dir + name + gb_prefix
    save_to_new_directory(gb1, gb2, gb3, gb_path_to_save)

    gn1, gn2, gn3 = convert_to_unit8(gn_1, gn_2, gn_3)
    # gaussian noise prefix and pathing
    gn_prefix = "_gaussian_noise"
    gn_path_to_save = distorted_dataset_dir + name + gn_prefix
    save_to_new_directory(gn1, gn2, gn3, gn_path_to_save)

    sp1, sp2, sp3 = convert_to_unit8(sp_1, sp_2, sp_3)
    # salt and pepper prefix and pathing
    sp_prefix = "_salt_and_pepper"
    sp_path_to_save = distorted_dataset_dir + name + sp_prefix
    save_to_new_directory(sp1, sp2, sp3, sp_path_to_save)

    s1, s2, s3 = convert_to_unit8(s_1, s_2, s_3)
    # speckle prefix and pathing
    s_prefix = "_sparkle"
    s_path_to_save = distorted_dataset_dir + name + s_prefix
    save_to_new_directory(s1, s2, s3, s_path_to_save)


# convert floating-point images
def convert_to_unit8(floating_1, floating_2, floating_3):
    # img = cv2.convertScaleAbs(image, alpha=255.0)
    converted_1 = np.array(255 * floating_1, dtype=np.uint8)
    converted_2 = np.array(255 * floating_2, dtype=np.uint8)
    converted_3 = np.array(255 * floating_3, dtype=np.uint8)
    return converted_1, converted_2, converted_3


def save_to_new_directory(image_1, image_2, image_3, path_to_save):
    # designed to take three image distortions that were applied to a
    # single image, with the appropriate path and file name, then allocate
    # a final prefix to the appropriate image with a file extension
    prefix_1 = path_to_save + "_1.png"
    prefix_2 = path_to_save + "_2.png"
    prefix_3 = path_to_save + "_3.png"

    # saving the file with the original name, the new distortion
    # prefix to the new location, e.g "./distorted_dataset/image_1_gb_1.png
    # -> i.e the first variance of image one with gaussian blur applied
    cv2.imwrite(prefix_1, image_1)
    print("saving prefix 1")
    time.sleep(0.02)
    # cv2.imwrite(prefix_2, image_2)
    # print("saving prefix 2")
    # time.sleep(0.02)
    cv2.imwrite(prefix_3, image_3)
    print("saving prefix 3")
    time.sleep(5)
    #cv2.waitKey(0)


i = 0

for image_in_dataset in os.listdir(dataset_dir):

    image_path = dataset_dir + image_in_dataset
    imported_image = Image.open(image_path)
    # convert to numpy array
    converted_to_np = np.asarray(imported_image)

    i += 1
    image_name = str(i)
    print("processing image: " + image_name)
    #image_name = os.path.splitext(image_in_dataset)[0]
    distort_and_save_images(converted_to_np, image_name)
