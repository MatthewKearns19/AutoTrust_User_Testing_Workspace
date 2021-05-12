import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as im


def classify_image(image_path):

    loaded_image = load_img('./screenshots/pre_defined_screenshots/homepage.png', target_size=(224, 224))

    model = load_model('./models/Sequential_Image_Distortion_Classifier.h5')
    time.sleep(10)

    img_array = im.img_to_array(loaded_image)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    image = tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

    feature_prediction = model.predict(image)
    print(feature_prediction.shape)

    # for prediction in feature_prediction:
    #     print([prediction])

    for i in feature_prediction:

        if [i][0][0] > 0.95:
            print("image features are classified blur distortion.")
        if [i][0][1] > 0.95:
            print("image features are classified color distortion")
        if [i][0][2] > 0.95:
            print("image features are classified JPEG compression")
        if [i][0][3] > 0.95:
            print("image features are classified as high resolution")
        if [i][0][4] > 0.95:
            print("image features are classified as noise distortion")
        if [i][0][5] > 0.95:
            print("image features are classified as spatial distortion")
