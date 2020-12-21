from behave import *
from functions.webdriver_functions import find_element_by_xpath
from variables.browser_elements import welcome_element
from functions.home_page_fuctions import execute_homepage_navigation

# from functions.webdriver_functions import screenshot


use_step_matcher("re")


# This defines the use action from our feature file, and then passing this captured data to our functions directory
@when("The user navigates to the (?P<homepage_url>.+)")
def homepage_navigation(context, homepage_url):
    execute_homepage_navigation(context, homepage_url)


@then("Then the user can see the (?P<welcome_text>.+)")
def locate_welcome_text(context, welcome_text):
    # must be .text
    xpath_found_output = find_element_by_xpath(context, welcome_element).text
    assert xpath_found_output == welcome_text

    """ when an element is found, we then need to call our npm package, to screenshot the current browser state 
        and store it in our /data/test_screenshot_outputs directory. After this is captured, we want to retrieve 
        this image and run our node.js npm package command to retrieve a ui interpretation result 
        e.g compare(Homepage1, Homepage2)"""
