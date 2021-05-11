import os

from behave import *
from functions.main_functions_flow import find_element_by_xpath, screenshot
from image_classifiers.python_image_classifier_binary import compare_page_location_similarity
from variables.browser_elements import welcome_element
from functions.main_functions_flow import execute_homepage_navigation
import time

use_step_matcher("re")


# This defines the step outlined from our feature file

@when("The user navigates to the (?P<homepage_url>.+)")
def homepage_navigation(context, homepage_url):
    execute_homepage_navigation(context, homepage_url)
    time.sleep(2)


@then("the user can see the (?P<welcome_text>.+)")
def locate_welcome_text(context, welcome_text):
    element_found_by_xpath = find_element_by_xpath(context, welcome_element)
    time.sleep(3)
    text_found = element_found_by_xpath.text
    print(text_found)
    assert text_found == welcome_text


@step("the user visually compares the (?P<screenshotted_page>.+)")
def compare_chosen_image(context, screenshotted_page):
    """ when an element is found, we then need to call our npm package, to screenshot the current browser state
        and store it in our /screenshots/browser_screenshot_outputs directory. After this is captured, we want to retrieve
        this image and run our node.js npm package command to retrieve a ui interpretation result
        e.g compare(Homepage1, Homepage2)"""

    page_name = screenshotted_page

    screenshot(context, page_name)
    time.sleep(3)
    compare_page_location_similarity(context, page_name)
