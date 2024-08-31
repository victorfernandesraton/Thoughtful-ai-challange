from pathlib import Path

import httpx

from domain import Article


def download_image(article: Article) -> None:
    response = httpx.get(article.img_url)
    response.raise_for_status()

    file_path = article.get_image_path(response.content)
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as file:
        file.write(response.content)
