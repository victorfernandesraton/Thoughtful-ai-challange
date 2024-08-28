from robocorp.tasks import task

from browser import Browser


@task
def search_news(query, category, months=0):
    browser = Browser()
    browser.open_url("https://apnews.com/")


if __name__ == "__main__":
    search_news("brazil", "Finance")
