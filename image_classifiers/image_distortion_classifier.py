# confusion matrix source: https://deeplizard.com/learn/video/HDom7mAxCdc

import os
import cv2
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as im
import itertools
import matplotlib.pyplot as plt
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.metrics import confusion_matrix

# from variables.app_variables import image_quality_distortion_model_path, \
#     confusion_matrix_assessment_path, png_file_extension, \
#     confusion_matrix_output_path, matrix_extension, assessment_high_resolution_assessment_path, artifacts_path, \
#     screenshot_results_path
chrome_executable_path = '/usr/local/bin/chromedriver.exech'
pre_defined_screenshot_path = './screenshots/pre_defined_screenshots/'
screenshot_results_path = './screenshots/browser_screenshot_outputs/'
failed_comparisons_path = './screenshots/failed_comparisons/'
failed_file_extension = "_failed_comparison.png"
png_file_extension = ".png"
image_quality_distortion_model_path = './models/Sequential_Image_Distortion_Classifier.h5'
confusion_matrix_assessment_path = './confusion_matrix_assessment/model_classes/'
assessment_high_resolution_assessment_path = './confusion_matrix_assessment/model_classes/high_resolution/'
confusion_matrix_output_path = './confusion_matrix_assessment/confusion_matrix_output/'
matrix_extension = '_confusion_matrix.png'
artifacts_path = './artifacts/'
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
    plt.xlabel('Predicted label of image quality/distortion')

    path_to_save_matrix_plot = confusion_matrix_output_path + image_name + matrix_extension
    print('For local testing, saving matrix at the location: ' + path_to_save_matrix_plot)

    confusion_matrix_artifacts_path = artifacts_path + image_name + matrix_extension
    print('For CI/DC server integration, saving matrix at the location: ' + confusion_matrix_artifacts_path)

    plt.savefig(path_to_save_matrix_plot)
    plt.savefig(confusion_matrix_artifacts_path)


# crates the confusion matrix and calls plot_and_save_confusion_matrix above.
# the image name is passed for saving the
def create_confusion_matrix(image_name):
    test_path = confusion_matrix_assessment_path
    test_batches = ImageDataGenerator(preprocessing_function=preprocess_input) \
        .flow_from_directory(directory=test_path, target_size=(224, 224),
                             classes=['blur', 'color_distortion', 'compression',
                                      'high_resolution', 'noise', 'spatial_distortion'],
                             batch_size=10, shuffle=False)

    assessment_predictions = model.predict(x=test_batches, steps=len(test_batches), verbose=0)

    cm = confusion_matrix(y_true=test_batches.classes, y_pred=np.argmax(assessment_predictions, axis=-1))

    matrix_title = "Distortion Classifier Confusion Matrix Assessment for '{}'".format(image_name)
    plot_labels = ['blur', 'color', 'compression', 'high res', 'noise', 'spatial']
    plot_and_save_confusion_matrix(image_name, cm=cm, classes=plot_labels, title=matrix_title)


# classify the image quality with the CNN Distortion classifier,
# called from our test script functions
def classify_image_quality(screenshotted_image_path, image_name):
    image_path = screenshotted_image_path
    # load image as RBG with defined dimensions for model
    loaded_image = load_img(image_path, target_size=(224, 224))

    img_array = im.img_to_array(loaded_image)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    image = tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)

    feature_prediction = model.predict(image)
    np.round(feature_prediction)
    print('feature prediction model output shape: ' + str(feature_prediction.shape))

    final_prediction = None

    for class_predictions in feature_prediction:
        prediction_list = []
        for class_prediction in class_predictions:
            prediction_list.append(class_prediction)
        max_prediction_location = prediction_list.index(max(prediction_list))

        classes = ['blur distortion', 'color distortion', 'JPEG compression',
                   'high resolution', 'noise distortion', 'spatial distortion']

        final_prediction = classes[max_prediction_location]
        print('image features are classified as {}'.format(final_prediction))

    if final_prediction != 'high resolution':

        # write image to the high resolution folder to be assessed in a confusion matrix
        new_image_path_for_confusion_matrix = os.path.join(assessment_high_resolution_assessment_path,
                                                           image_name + png_file_extension)

        image_to_store_in_high_res_folder = cv2.imread(screenshotted_image_path)
        cv2.imwrite(new_image_path_for_confusion_matrix, image_to_store_in_high_res_folder)
        create_confusion_matrix(image_name)

        assert final_prediction != 'high resolution', \
            "The captured image labeled '{}' in your pre-defined images has failed " \
            "image quality assessment for distortion. Distortion of type '{}' was " \
            "classified instead of 'high resolution'".format(image_name, final_prediction)


def assess_and_classify_image_quality(page_name):
    image_name = page_name
    screenshotted_image = os.path.join(screenshot_results_path, image_name + png_file_extension)
    # assess the image that was screenshotted from the browser
    classify_image_quality(screenshotted_image, image_name)


assess_and_classify_image_quality('./screenshots/pre_defined_screenshots/landing_page.png')
