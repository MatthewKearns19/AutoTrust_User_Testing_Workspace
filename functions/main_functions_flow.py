import os
import time
from selenium.webdriver.support.wait import WebDriverWait

from variables.app_variables import screenshot_results_path, png_file_extension


def find_element_by_xpath(context, element):
    by_xpath = 'find_element_by_xpath'
    try:
        found_element_value = WebDriverWait(context.browser, 10)\
            .until(lambda browser: getattr(browser, by_xpath)(element))
        return found_element_value
    except Exception as e:
        #context.exe = e
        print('{} not found'.format(element))


def screenshot(context, page_name):
    time.sleep(1)
    path_to_save_screenshot = os.path.join(screenshot_results_path, page_name + png_file_extension)
    context.browser.save_screenshot(path_to_save_screenshot)
    time.sleep(1)


def execute_homepage_navigation(context, homepage_url):
    context.browser.get(homepage_url)
