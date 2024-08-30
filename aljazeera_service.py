from datetime import datetime
from enum import Enum
from typing import List

from bs4 import BeautifulSoup
from robocorp import log
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser
from domain import Article


class AljazeeraSelectOrderOptions(Enum):
    DATE = "date"
    RELEVANCE = "relevance"


class AljazeeraService:
    DOMAIN = "https://www.aljazeera.com/"
    BTN_SEARCH_SELECTOR = (By.XPATH, "//button/span[text()='Click here to search']/..")
    INPUT_SEARCH_SELECTOR = (By.XPATH, "//input[@placeholder='Search']")
    SELECT_ORDER_BY_SELECTOR = (By.XPATH, "//select[@id='search-sort-option']")
    SELECT_ARTICLES_SELECTOR = (By.CSS_SELECTOR, ".search-result__list")

    def __init__(self, browser: Browser, timeout=30):
        self.browser = browser
        self.timeout = timeout
        self.waiter = WebDriverWait(self.browser.driver, self.timeout)
        self.browser.open_url(self.DOMAIN)

    def execute(self, query: str, option="date") -> List[Article]:
        self.search_for_query(query)
        self.select_order_by(AljazeeraSelectOrderOptions(option))

        return self.extract_content(query)

    def __validate_string_to_option_enum(value_str):
        enum_member = AljazeeraSelectOrderOptions(value_str)
        return enum_member

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

    def select_order_by(self, option: AljazeeraSelectOrderOptions):
        select_el = self.waiter.until(
            EC.presence_of_element_located(self.SELECT_ORDER_BY_SELECTOR)
        )
        select = Select(select_el)
        select.select_by_value(option.value)

    def extract_content(self, query: str) -> List[Article]:
        result = []
        article_div = self.waiter.until(
            EC.presence_of_element_located(self.SELECT_ARTICLES_SELECTOR)
        )
        soup = BeautifulSoup(article_div.get_attribute("outerHTML"), "html.parser")

        # Find all articles
        articles = soup.find_all(
            "article",
            class_="gc u-clickable-card gc--type-customsearch#result gc--list gc--with-image",
        )

        # Iterate over each article and extract details
        for article in articles:
            title_tag = article.find("h3", class_="gc__title").find("a")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            link = title_tag["href"] if title_tag else "No link"

            excerpt_tag = article.find("div", class_="gc__excerpt").find("p")
            content = excerpt_tag.get_text(strip=True) if excerpt_tag else "No content"

            date_tag = article.find("div", class_="gc__date__date")
            date = (
                datetime.strptime(
                    date_tag.get_text(strip=True)[-11:], "%d %b %Y"
                ).date()
                if date_tag
                else None
            )

            post = Article(
                search_query=query,
                title=title,
                description=content,
                url=link,
                date=date,
            )
            result.append(post)
