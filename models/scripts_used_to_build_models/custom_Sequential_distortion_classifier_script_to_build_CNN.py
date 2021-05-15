get_ipython().magic('matplotlib inline')
import os
import numpy as np
import tensorflow as tf
import random as python_random
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Activation, Dense, Dropout, Flatten, Conv2D, BatchNormalization, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model
from keras.utils.generic_utils import get_custom_objects

from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions

import cv2
import matplotlib.pyplot as plt
from numpy import expand_dims
import warnings
import pandas as pd
import itertools

# set the random seed for reproducability
os.environ['PYTHONHASHSEED'] = '0'

np.random.seed(123)

python_random.seed(123)

tf.random.set_seed(1234)

train_path = './train'
valid_path = './validation'
test_path = './test'

train_batches = ImageDataGenerator(preprocessing_function=preprocess_input) \
    .flow_from_directory(directory=train_path, target_size=(224,224),
        classes=['blur', 'color_distortion', 'compression', 'high_resolution',
        'noise', 'spatial_distortion'], batch_size=10)

valid_batches = ImageDataGenerator(preprocessing_function=preprocess_input) \
    .flow_from_directory(directory=valid_path, target_size=(224,224),
        classes=['blur', 'color_distortion', 'compression', 'high_resolution',
        'noise', 'spatial_distortion'], batch_size=10)

test_batches = ImageDataGenerator(preprocessing_function=preprocess_input) \
    .flow_from_directory(directory=test_path, target_size=(224,224),
        classes=['blur', 'color_distortion', 'compression', 'high_resolution',
        'noise', 'spatial_distortion'], batch_size=10, shuffle=False)


model = Sequential([
    Conv2D(filters=32, kernel_size=(3, 3), activation='relu',
        padding = 'same', input_shape=(224,224,3)),
    MaxPool2D(pool_size=(2, 2), strides=2),
    Conv2D(filters=64, kernel_size=(3, 3), activation='relu',
        padding = 'same'),
    MaxPool2D(pool_size=(2, 2), strides=2),
    Flatten(),
    Dense(units=4, activation='softmax')
])

model.summary()

#specifying a low learning rate
model.compile(optimizer=Adam(learning_rate=0.0001),
    loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x=train_batches,
    steps_per_epoch=len(train_batches),
    validation_data=valid_batches,
    validation_steps=len(valid_batches),
    epochs=10,
    verbose=2
)



predictions = model.predict(x=test_batches, steps=len(test_batches), verbose=0)
for i in predictions:
    print([i])
