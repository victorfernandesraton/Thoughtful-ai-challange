from robocorp.tasks import task

from aljazeera_service import AljazeeraService
from browser import Browser


@task
def search_news():
    browser = Browser()
    browser.set_webdriver()
    service = AljazeeraService(browser)
    service.execute("brazil")


if __name__ == "__main__":
    search_news()
