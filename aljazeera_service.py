from enum import Enum

from robocorp import log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser


class AljazeeraSelectOrderOptions(Enum):
    DATE = "date"
    RELEVANCE = "relevance"


class AljazeeraService:
    DOMAIN = "https://www.aljazeera.com/"
    BTN_SEARCH_SELECTOR = (By.XPATH, "//button/span[text()='Click here to search']/..")
    INPUT_SEARCH_SELECTOR = (By.XPATH, "//input[@placeholder='Search']")
    SELECT_ORDER_BY_SELECTOR = (By.XPATH, "//select[@id='search-sort-option']")

    def __init__(self, browser: Browser, timeout=30):
        self.browser = browser
        self.timeout = timeout
        self.waiter = WebDriverWait(self.browser.driver, self.timeout)
        self.browser.open_url(self.DOMAIN)

    def search_for_query(self, query: str):
        btn_serach = self.waiter.until(
            EC.presence_of_element_located(self.BTN_SEARCH_SELECTOR)
        )
        log.info("Found button search")
        btn_serach.click()

        input_search = self.waiter.until(
            EC.presence_of_element_located(self.INPUT_SEARCH_SELECTOR)
        )

        log.info("Found input search")

        input_search.clear()
        input_search.send_keys(query)
        input_search.send_keys(Keys.ENTER)

        self.select_order_by(AljazeeraSelectOrderOptions.RELEVANCE)

    def select_order_by(self, option: AljazeeraSelectOrderOptions):
        select_el = self.waiter.until(
            EC.presence_of_element_located(self.SELECT_ORDER_BY_SELECTOR)
        )
        select = Select(select_el)
        select.select_by_value(option.value)

    def extract_content(self):
        pass
