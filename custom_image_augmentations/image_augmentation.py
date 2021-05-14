import cv2
from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from PIL import Image
import PIL
import argparse
import os
import time


parser = argparse.ArgumentParser(description='Starting Image distortion generator')
parser.add_argument('-load_image_directory', default='./dataset/', type=str)
parser.add_argument('-directory_to_save_to', default='./augmented_images/', type=str)

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


def load_image(img):
    load_img(img)


# convert the loaded image to a 3d numpy array and expand samples
def convert_to_3d_numpy_array(loaded_img):
    data = img_to_array(loaded_img)
    sample_data = expand_dims(data, 0)
    return sample_data


# prepare iterator using .flow() to generate random batches of transferred images
def prepare_iterator(sample, directory, image_prefix):
    iterator = data_generator.flow(
        sample,
        save_to_dir=directory,
        save_prefix=image_prefix,
        shuffle=False)
    return iterator


data_generator = ImageDataGenerator(horizontal_flip=True,
                                    rescale=1/224.)

i = 0

for image_in_dataset in os.listdir(dataset_dir):
    time.sleep(0.02)

    image_path = dataset_dir + image_in_dataset
    imported_image = load_img(image_path)
    # convert to numpy array
    samples = convert_to_3d_numpy_array(imported_image)

    i += 1
    image_name = os.path.splitext(image_in_dataset)[0]
    print("processing image: " + image_name)

    prefix = image_name + "aug"
    prepared_iterator = prepare_iterator(samples, args.directory_to_save_to, prefix)

    # generate augmented images and save to augmented_images folder
    for i in range(1):
        batch = prepared_iterator.next()
        image = batch[0].astype('uint8')
