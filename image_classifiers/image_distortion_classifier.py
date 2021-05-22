# confusion matrix source: https://deeplizard.com/learn/video/HDom7mAxCdc

import os
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as im
import itertools
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from variables.app_variables import image_quality_distortion_model_path, \
    png_file_extension, confusion_matrix_output_path, matrix_extension, \
    artifacts_path, screenshot_results_path


# loading the Image Quality Classifier
model = load_model(image_quality_distortion_model_path)
time.sleep(10)


def plot_and_save_confusion_matrix(image_name, cm,
                                   classes, title=''):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.get_cmap('Blues'))
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    print('Performing Confusion matrix of image quality assessment')

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label for each feature class')
    plt.xlabel('Predicted label of image quality/distortion\n')

    path_to_save_matrix_plot = confusion_matrix_output_path + image_name + matrix_extension
    print('For local testing, saving matrix at the location: ' + path_to_save_matrix_plot)

    confusion_matrix_artifacts_path = artifacts_path + image_name + matrix_extension
    print('For CI/DC server integration, saving matrix at the location: ' + confusion_matrix_artifacts_path)

    plt.savefig(path_to_save_matrix_plot)
    plt.savefig(confusion_matrix_artifacts_path)


# crates the confusion matrix and calls plot_and_save_confusion_matrix above.
# the image name is passed for saving the
def create_confusion_matrix(image_name, max_prediction_location):
    true_labels = [0, 1, 2, 3, 3, 4, 5]
    # replace the high res true label position with the predicted label position,
    # to plot true vs. predicted values on the confusion matrix, e.g if the model
    # predicted blur distortion, that has an index of 0, then the new predicted
    # labels would be [0, 1, 2, 3, 0, 4, 5]
    labels_after_predicted = true_labels

    labels_after_predicted[4] = max_prediction_location

    cm = confusion_matrix(y_true=true_labels, y_pred=labels_after_predicted)

    matrix_title = "Distortion Classifier Confusion Matrix for '{}'".format(image_name)
    plot_labels = ['blur', 'color', 'compression', 'high res', 'noise', 'spatial']
    plot_and_save_confusion_matrix(image_name, cm=cm, classes=plot_labels, title=matrix_title)


# classify the image quality with the CNN Distortion classifier,
# called from our test script functions
def classify_image_quality(screenshotted_image_path, image_name):
    image_path = screenshotted_image_path
    # load image as RBG with defined dimensions for model -> model was trained on 244 x 244
    loaded_image = load_img(image_path, target_size=(224, 224))
    # convert to a nupmy array and pre-process the
    # expanded dimensions before passing to the model
    img_array = im.img_to_array(loaded_image)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    image = tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

    feature_prediction = model.predict(image)
    np.round(feature_prediction)

    final_prediction = None

    # extract each prediction from the numpy array outputted,
    # and then find the prediction with the highest predicted value
    for class_predictions in feature_prediction:
        prediction_list = []
        for class_prediction in class_predictions:
            prediction_list.append(class_prediction)
        max_prediction_location = prediction_list.index(max(prediction_list))

        classes = ['blur distortion', 'color distortion', 'JPEG compression distortion',
                   'high resolution', 'noise distortion', 'spatial distortion']
        # use the location of the highest predicted prediction to get the
        # corresponding class name that the model was trained on
        final_prediction = classes[max_prediction_location]
        print('image features are classified as {}'.format(final_prediction))

        create_confusion_matrix(image_name, max_prediction_location)

    # if the image is not high resolution then fail the test
    if final_prediction != 'high resolution':

        assert final_prediction == 'high resolution', \
            "The captured image labeled '{}' in your pre-defined images has failed " \
            "image quality assessment for distortion. Distortion of type '{}' was " \
            "classified instead of 'high resolution'".format(image_name, final_prediction)


def assess_and_classify_image_quality(context, page_name):
    image_name = page_name
    screenshotted_image = os.path.join(screenshot_results_path, image_name + png_file_extension)
    # assess the image that was screenshotted from the browser
    classify_image_quality(screenshotted_image, image_name)
