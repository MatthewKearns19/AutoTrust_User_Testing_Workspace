# this is our environment file to work with our environment executables
from selenium import webdriver
from variables.app_variables import chrome_executable_path, screenshot_results_path, \
    failed_comparisons_path, artifacts_path
import os
import time


def before_all(context):
    """ this will be called to set up our chrome driver environment before each test sequence """

    options = webdriver.ChromeOptions()
    options.add_argument("--test-type")
    options.add_argument("--headless")
    options.binary_location = "/usr/bin/google-chrome"

    # context.browser = webdriver.Chrome(chrome_executable_path, port=9515, options=options,
    #                                    keep_alive=False)

    context.browser = webdriver.Chrome(chrome_executable_path, options=options)

    context.browser.implicitly_wait(10)
    #context.browser.set_window_size(1920, 1080, context.browser.window_handles[0])
    context.browser.set_window_size(1528, 768, context.browser.window_handles[0])

    os.mkdir(screenshot_results_path)
    time.sleep(1)
    os.mkdir(failed_comparisons_path)
    time.sleep(1)
    os.mkdir(artifacts_path)
    time.sleep(1)


def after_all(context):
    context.browser.quit()
