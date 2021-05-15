# this is our environment file to work with our environment executables
from selenium import webdriver
from variables.app_variables import chrome_executable_path


def before_all(context):
    """ this will be called to set up our chrome driver environment before each test sequence """

    options = webdriver.ChromeOptions()
    options.add_argument("--test-type")
    options.add_argument("--headless")

    # context.browser = webdriver.Chrome(chrome_executable_path, port=9515, options=options,
    #                                    keep_alive=False)

    context.browser = webdriver.Chrome(chrome_executable_path, options=options)

    context.browser.implicitly_wait(10)
    #context.browser.set_window_size(1920, 1080, context.browser.window_handles[0])
    context.browser.set_window_size(1528, 768, context.browser.window_handles[0])


def after_all(context):
    context.browser.quit()
