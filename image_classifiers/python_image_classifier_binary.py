# source 1 = https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
# source 2 = https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/

import os
import cv2
from skimage.measure import compare_ssim
import imutils
import shutil

from variables.app_variables import screenshot_results_path, png_file_extension, failed_comparisons_path, \
	failed_file_extension


def compare_images(context, page_name):

	# temporarily using a distorted pre-defined screenshot to compare against the captured
	# screenshot, as the browser currently displays a non-distorted (true) image.
	test_path = "screenshots/pre_defined_screenshots/test.png"
	screenshotted_path = os.path.join(screenshot_results_path, page_name + png_file_extension)
	image1 = cv2.imread(screenshotted_path)
	image2 = cv2.imread(test_path)

	# convert the images to grayscale
	image1_grayscale = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
	image2_grayscale = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

	# passing the two grayscale images into compare_ssim to find the
	# Structural Similarity Index (SSIM)
	(ssim_score, diff) = compare_ssim(image1_grayscale, image2_grayscale, full=True)
	image_diff = (diff * 255).astype("uint8")
	print("Similarity score: {}".format(ssim_score))

	# threshold the difference image, followed by
	# finding contours to
	# obtain the regions of the two input images that differ
	# by comparing the difference
	threshold = cv2.threshold(image_diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = imutils.grab_contours(contours)

	for contour in contours:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(contour)
		# now drawing the bounding box to highlight the difference area
		cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# cv2.imshow("Modified", image2)
	# save the image
	failed_image_path = os.path.join(failed_comparisons_path, page_name + failed_file_extension)
	cv2.imwrite(failed_image_path, image2)
	cv2.waitKey(0)

	# cv2.destroyAllWindows()
