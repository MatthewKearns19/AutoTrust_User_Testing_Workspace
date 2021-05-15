get_ipython().magic('matplotlib inline')
import os
import numpy as np
import tensorflow as tf
import random as python_random
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications import imagenet_utils
from sklearn.metrics import confusion_matrix
from tensorflow.keras.regularizers import l2

import cv2
import matplotlib.pyplot as plt
from numpy import expand_dims
import warnings
import pandas as pd
import itertools
%matplotlib inline


os.environ['PYTHONHASHSEED'] = '0'

np.random.seed(123)

python_random.seed(123)

tf.random.set_seed(1234)


train_path = './train'
valid_path = './validation'
test_path = './test'

train_batches = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet.preprocess_input) \
    .flow_from_directory(directory=train_path, target_size=(224,224),
    classes=['blur', 'color_distortion', 'compression', 'high_resolution',
    'noise', 'spatial_distortion'], batch_size=32)

valid_batches = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet.preprocess_input) \
    .flow_from_directory(directory=valid_path, target_size=(224,224),
    classes=['blur', 'color_distortion', 'compression', 'high_resolution',
    'noise', 'spatial_distortion'], batch_size=32)

test_batches = ImageDataGenerator(
preprocessing_function=tf.keras.applications.mobilenet.preprocess_input) \
    .flow_from_directory(directory=test_path, target_size=(224,224),
    classes=['blur', 'color_distortion', 'compression', 'high_resolution',
    'noise', 'spatial_distortion'], batch_size=32, shuffle=False)


mobile_model = tf.keras.applications.mobilenet.MobileNet()

# print the summary before fine-tuning
mobile_model.summary()

# remove the sixth-to-last layer
x = mobile_model.layers[-6].output

# passing all previous layers up to the sixth-to-last
# layer as our output layer
output = Dense(units=6, activation='softmax')(x)

# using this new output, which also defines
# the previous layers, as our model output
model = Model(inputs=mobile_model.input, outputs=output)

# now freezing the last 23 layers
for layer in model.layers[:-23]:
    layer.trainable = False

model.summary()

# may need to set categorical_crossentropy as a custom object in our keras instance
#get_custom_objects().update({'categorical_cross_entropy': categorical_crossentropy})
model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])


model.fit(x=train_batches,
            steps_per_epoch=len(train_batches),
            validation_data=valid_batches,
            validation_steps=len(valid_batches),
            epochs=3,
            verbose=2
)

predictions = model.predict(x=test_batches, steps=len(test_batches), verbose=0)
for i in predictions:
    print([i])
