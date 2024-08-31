from os import getcwd, path
from pathlib import Path

from robocorp import workitems
from robocorp.tasks import task

from aljazeera_service import AljazeeraService
from browser import Browser
from exporter import ExporterService

# Define the directory to search in
directory_path = Path(path.join(getcwd(), "extracted"))


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

    item = workitems.outputs.create(save=False)

    for index, file_path in enumerate(directory_path.glob("images/*")):
        item.add_file(file_path, name=f"document-{index}")

    for index, file_path in enumerate(directory_path.glob("excel/*")):
        item.add_file(file_path, name=f"document-{index}")
    item.add_file("local.log")
    item.save()


def proccess_news():
    pass


if __name__ == "__main__":
    search_news()
