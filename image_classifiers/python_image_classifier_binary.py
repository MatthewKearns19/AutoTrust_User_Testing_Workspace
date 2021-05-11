# source 1 = https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
# source 2 = https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/

import os
import cv2
#from skimage.measure import compare_ssim
from skimage.metrics import structural_similarity
import imutils
import time

from variables.app_variables import screenshot_results_path, png_file_extension, \
	failed_comparisons_path, pre_defined_screenshot_path, failed_file_extension


def compare_page_location_similarity(context, image_name):

	# temporarily using a distorted pre-defined screenshot to compare against the captured
	# screenshot, as the browser currently displays a non-distorted (true) image.
	#pre_defined_screenshot = "screenshots/pre_defined_screenshots/homepage2.png"
	pre_defined_screenshot = os.path.join(pre_defined_screenshot_path, image_name + png_file_extension)
	image1 = cv2.imread(pre_defined_screenshot)
	screenshotted_image = os.path.join(screenshot_results_path, image_name + png_file_extension)
	image2 = cv2.imread(screenshotted_image)

	# convert the images to grayscale
	image1_grayscale = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	image2_grayscale = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

	# passing the two grayscale images into compare_ssim to find the
	# Structural Similarity Index (SSIM)
	# use structural_similarity instead of compare_ssim for skimage==0.18.1
	(ssim_score, diff) = structural_similarity(image1_grayscale, image2_grayscale, full=True)
	print("Similarity score: {}".format(ssim_score))


	# if the similarity ratio is less that 1:1
	if ssim_score < 1.0:
		# diff is represented as a floating point data type in the range [0,1]
		# as it was returned from compare_ssim, so we must convert the array to
		# 8-bit unsigned integers in the range [0,255] before we can use it with cv2
		image_diff = (diff * 255).astype("uint8")

		# threshold the difference image, followed by finding contours to obtain the regions
		# of the two input images that differ by comparing the difference
		threshold = cv2.threshold(image_diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
		contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)

		for contour in contours:
			area = cv2.contourArea(contour)
			if area > 20:
				# compute the bounding box of the contour
				(x, y, w, h) = cv2.boundingRect(contour)
				# now drawing the bounding box to highlight the difference area,
				# un-comment image1 below for further debugging if necessary
				# cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
				cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

		# save the image
		failed_image_path = os.path.join(failed_comparisons_path, image_name + failed_file_extension)
		cv2.imwrite(failed_image_path, image2)
