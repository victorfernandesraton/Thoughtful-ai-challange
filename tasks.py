from robocorp import workitems
from robocorp.tasks import task

from aljazeera_service import AljazeeraService
from browser import Browser
from exporter import ExporterService


@task
def search_news():
    browser = Browser()
    browser.set_webdriver()
    service = AljazeeraService(browser)
    for item in workitems.inputs:
        results = service.execute(
            item.payload["query"], item.payload["order_by"], item.payload["months"]
        )
        exportation = ExporterService(results)
        exportation.execute()
