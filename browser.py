import logging

from selenium import webdriver
from selenium.webdriver import ChromeOptions


class Browser:
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)

    def set_chrome_options(self):
        options = ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-web-security")
        options.add_argument("--start-maximized")
        options.add_argument("--remote-debugging-port=9222")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        return options

    def set_webdriver(self):
        self.driver = webdriver.Chrome(options=self.set_chrome_options())

    def open_url(self, url: str, screenshot: str = None):
        self.driver.get(url)
        if screenshot:
            self.driver.get_screenshot_as_file(screenshot)

    def driver_quit(self):
        if self.driver:
            self.driver.quit()

    def full_page_screenshot(self, url):
        self.driver.get(url)
        page_width = self.driver.execute_script("return document.body.scrollWidth")
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(page_width, page_height)
        self.driver.save_screenshot("screenshot.png")
        self.driver.quit()
