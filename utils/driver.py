from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

def get_driver():
    options = FirefoxOptions()
    options.add_argument('--headless')  # Ejecutar sin UI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver