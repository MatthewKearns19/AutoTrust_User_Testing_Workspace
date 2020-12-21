import time
from selenium import webdriver
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui

'''
def find_element_by_xpath(context, wanted_element_value):

    driver = webdriver.Chrome()
    found_element_value = WebDriverWait(driver, 10).until(driver.find_element(By.XPATH, wanted_element_value))
    return found_element_value
    '''


''' this is where our wanted elements will be searched for in the browser,
    for example the welcome element passed from our homepage step'''


def find_element_by_xpath(context, element):
    by_xpath = 'find_element_by_xpath'
    try:
        """driver.implicitly_wait(10)
        found_element_value = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_element_by(By.XPATH, wanted_element_value))"""
        found_element_value = WebDriverWait(context.browser, 10).until(lambda browser: getattr(browser, by_xpath)
        (element))
        context.exe = None
        return found_element_value
    except Exception as e:
        context.exe = e
        print('{} not found'.format(element))
