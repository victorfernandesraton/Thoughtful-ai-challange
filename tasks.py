from robocorp import workitems
from robocorp.tasks import task

from aljazeera_service import AljazeeraService
from browser import Browser


@task
def search_news():
    browser = Browser()
    browser.set_webdriver()
    service = AljazeeraService(browser)
    for item in workitems.inputs:
        results = service.execute(
            item.payload["query"], item.payload["order_by"], item.payload["months"]
        )
        print(len(results))


def proccess_news():
    pass


if __name__ == "__main__":
    search_news()
