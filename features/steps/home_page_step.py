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
    """
        Description: navigates to the homepage url, to open for extension and de-couple operations in further
        development, simply change the 'homepage_url' param  to 'url', move to a file for global general steps,
        and you can then define this step in any scenario, in any feature for any specified url to navigate to.
        The same operations will be executed but on a different url.
        :param homepage_url: The url of the sites homepage.
        :return: executes execute_homepage_navigation() function which executes the request in teh browser.
    """
    execute_homepage_navigation(context, homepage_url)
    time.sleep(2)


@then("the user can see the (?P<heading_text>.+)")
def locate_welcome_text(context, heading_text):
    """
        Description: navigates to the page welcome text, using the imported
        welcome_text browser DOM Xpath defined in variables -> browser elements.
        :param heading_text: The expected heading/subheading to find in the browser, used for assertion.
        :return: test assertion of the found welcome_element text against the expected heading_text param.
    """
    element_found_by_xpath = find_element_by_xpath(context, welcome_element)
    time.sleep(3)
    text_found = element_found_by_xpath.text
    print(text_found)
    assert text_found == heading_text


""" when an element is found, we then need to screenshot the current browser state and store it in our 
/screenshots/browser_screenshot_outputs directory. Then we need to compare the image, executed in the 
compare_page_location_similarity function, e.g., compare(pre_defined_homepage_image1, new_browser_homepage_image2)"""

@step("the user visually compares the (?P<screenshotted_page_location>.+)")
def compare_chosen_page_location_image(context, screenshotted_page_location):
    """
        Description: takes a screenshot of the current browser state at the specified page location.
        :param screenshotted_page_location: specified page location, used to tell the compare_page_location_similarity()
        function the name of the pre-defined screenshot that is to be used in comparison.
        :return: fail or pass if the compare_page_location_similarity() function fails or passes image comparison.
    """
    page_name = screenshotted_page_location
    screenshot(context, page_name)
    time.sleep(3)
    compare_page_location_similarity(context, page_name)


@step("the the location contains an image so assess the image quality (?P<screenshotted_page_location>.+)")
def assess_chosen_page_location_image_quality(context, screenshotted_page_location):
    """
        Description: uses the same screenshot of the page location captured in the last step, by defining the
        same pre-defined screenshot name, allowing the assess_and_classify_image_quality() to locate this image
        again in the browser_screenshot_outputs folder. Image Distortion Classification is then assessed.
        :param screenshotted_page_location: specified page location, passed to assess_and_classify_image_quality()
        function the name of the pre-defined screenshot that is to be used in comparison.
        :return: fail or pass if the assess_and_classify_image_quality() function fails or passes image comparison.
    """
    page_name = screenshotted_page_location
    screenshot(context, page_name)
    time.sleep(3)
    assess_and_classify_image_quality(context, page_name)
