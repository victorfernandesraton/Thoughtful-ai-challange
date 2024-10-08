from datetime import datetime
from enum import Enum
from typing import List

from bs4 import BeautifulSoup, PageElement
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from browser import Browser
from domain import Article, filter_articles_by_valid_months, valid_months_in_ratio
from locallogger import logger


class AljazeeraSelectOrderOptions(Enum):
    DATE = "date"
    RELEVANCE = "relevance"


class AljazeeraService:
    DOMAIN = "https://www.aljazeera.com/"
    BUTTON_SEARCH_SELECTOR = (
        By.XPATH,
        "//button/span[text()='Click here to search']/..",
    )
    INPUT_SEARCH_SELECTOR = (By.XPATH, "//input[@placeholder='Search']")
    SELECT_ORDER_BY_SELECTOR = (By.XPATH, "//select[@id='search-sort-option']")
    ARTICLES_SELECTOR = (By.CSS_SELECTOR, ".search-result__list")
    BUTTON_SHOW_MORE_SELECTOR = (By.CSS_SELECTOR, "button.show-more-button")
    DIV_LOADING_SELECTOR = (By.CSS_SELECTOR, "div.loading-animation")
    BUTTON_ACCEPT_COOKIE_SELECTOR = (
        By.CSS_SELECTOR,
        "button#onetrust-accept-btn-handler",
    )

    def __init__(self, browser: Browser, timeout=30):
        self.browser = browser
        self.timeout = timeout
        self.waiter = WebDriverWait(self.browser.driver, self.timeout)
        self.browser.open_url(self.DOMAIN)

    def execute(self, query: str, option="date", months=0) -> List[Article]:
        result = set()
        self.__click_accept_cookie()
        self.__search_for_query(query)
        self.__select_order_by(AljazeeraSelectOrderOptions(option))
        valid_months = valid_months_in_ratio(date=datetime.today().date(), ratio=months)
        while True:
            self.waiter.until_not(
                EC.presence_of_element_located(self.DIV_LOADING_SELECTOR)
            )
            chunk = self.__extract_content(query)
            filter_chunk = filter_articles_by_valid_months(
                articles=chunk, valid_months=valid_months
            )
            if len(filter_chunk):
                result.update(filter_chunk)
            last_chunk = chunk[-1]
            last_valid_month = valid_months[-1]
            if (
                last_chunk.date.year >= last_valid_month[0]
                and last_chunk.date.month >= last_valid_month[1]
            ):
                if self.__click_get_more():
                    continue
                else:
                    break

            break
        return list(result)

    def __click_get_more(self) -> bool:
        try:
            show_more_button = self.waiter.until(
                EC.presence_of_element_located(self.BUTTON_SHOW_MORE_SELECTOR)
            )
            self.browser.driver.execute_script(
                "arguments[0].scrollIntoView();", show_more_button
            )
            show_more_button.click()
            return True
        except (
            NoSuchElementException,
            TimeoutException,
            ElementClickInterceptedException,
        ):
            return False

    def __validate_string_to_option_enum(value_str):
        enum_member = AljazeeraSelectOrderOptions(value_str)
        return enum_member

    def __search_for_query(self, query: str):
        btn_serach = self.waiter.until(
            EC.visibility_of_element_located(self.BUTTON_SEARCH_SELECTOR)
        )
        logger.info("Found button search")
        btn_serach.click()

        input_search = self.waiter.until(
            EC.presence_of_element_located(self.INPUT_SEARCH_SELECTOR)
        )

        logger.info("Found input search")

        input_search.clear()
        input_search.send_keys(query)
        input_search.send_keys(Keys.ENTER)

    def __select_order_by(self, option: AljazeeraSelectOrderOptions):
        select_el = self.waiter.until(
            EC.presence_of_element_located(self.SELECT_ORDER_BY_SELECTOR)
        )
        select = Select(select_el)
        select.select_by_value(option.value)

    def __extract_content(self, query: str) -> List[Article]:
        result = []
        article_div = self.waiter.until(
            EC.presence_of_element_located(self.ARTICLES_SELECTOR)
        )
        soup = BeautifulSoup(article_div.get_attribute("outerHTML"), "html.parser")

        articles = soup.find_all(
            "article",
            class_="gc u-clickable-card gc--type-customsearch#result gc--list gc--with-image",
        )

        for article in articles:
            post = self.__get_article(query, article)
            result.append(post)

        return result

    def __click_accept_cookie(self):
        try:
            accept_cookie = self.waiter.until(
                EC.presence_of_element_located(self.BUTTON_ACCEPT_COOKIE_SELECTOR)
            )
            accept_cookie.click()
            logger.info("Accept cookies modal")
        except (
            NoSuchElementException,
            TimeoutException,
            ElementClickInterceptedException,
        ):
            logger.info("Not found accept cookies modal")

    def __get_article(self, query: str, article: PageElement) -> Article:
        title_tag = article.find("h3", class_="gc__title").find("a")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        link = title_tag["href"] if title_tag else "No link"

        excerpt_tag = article.find("div", class_="gc__excerpt").find("p")
        content = excerpt_tag.get_text(strip=True) if excerpt_tag else "No content"

        date_spans = article.select("footer div.gc__date__date > div > span")
        date = (
            datetime.strptime(date_spans[-1].text.rstrip()[-11:], "%d %b %Y").date()
            if len(date_spans)
            else None
        )
        img_tag = article.find("img", class_="article-card__image gc__image")
        img_url = img_tag["src"] if img_tag else None

        return Article(
            search_query=query,
            title=title,
            description=content,
            url=link,
            date=date,
            img_url=img_url,
        )
