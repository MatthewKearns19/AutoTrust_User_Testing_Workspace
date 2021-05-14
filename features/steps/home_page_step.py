import os

from behave import *
from functions.main_functions_flow import find_element_by_xpath, screenshot
from image_classifiers.binary_site_location_classifier import compare_page_location_similarity
from image_classifiers.image_distortion_classifier import assess_and_classify_image_quality
from variables.browser_elements import welcome_element
from functions.main_functions_flow import execute_homepage_navigation
import time

use_step_matcher("re")


# This defines the step outlined from our feature file

@when("The user navigates to the (?P<homepage_url>.+)")
def homepage_navigation(context, homepage_url):
    execute_homepage_navigation(context, homepage_url)
    time.sleep(2)


@then("the user can see the (?P<heading_text>.+)")
def locate_welcome_text(context, heading_text):
    element_found_by_xpath = find_element_by_xpath(context, welcome_element)
    time.sleep(3)
    text_found = element_found_by_xpath.text
    print(text_found)
    assert text_found == heading_text


@step("the user visually compares the (?P<screenshotted_page_location>.+)")
def compare_chosen_image(context, screenshotted_page_location):
    """ when an element is found, we then need to call our npm package, to screenshot the current browser state
        and store it in our /screenshots/browser_screenshot_outputs directory. After this is captured, we want to retrieve
        this image and run our node.js npm package command to retrieve a ui interpretation result
        e.g compare(Homepage1, Homepage2)"""

    page_name = screenshotted_page_location

    screenshot(context, page_name)
    time.sleep(3)
    compare_page_location_similarity(context, page_name)


@step("the the location contains an image so assess the image quality (?P<screenshotted_page_location>.+)")
def assess_chosen_page_location_image_quality(context, screenshotted_page_location):
    page_name = screenshotted_page_location

    screenshot(context, page_name)
    time.sleep(3)
    assess_and_classify_image_quality(context, page_name)
