from functions.webdriver_functions import find_element_by_xpath


def execute_homepage_navigation(context, homepage_url):
    context.browser.get(homepage_url)