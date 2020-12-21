# this is our environment file to work with our environment executables
from selenium import webdriver
from variables.variables import chrome_executable_path


def before_all(context):
    """ this will be called to set up our chrome driver environment before each test sequence """
    driver_settings = webdriver.ChromeOptions()
    context.browser = webdriver.Chrome(chrome_executable_path, port=9515, options=driver_settings,
                                       keep_alive=True)
    context.browser.implicitly_wait(10)
