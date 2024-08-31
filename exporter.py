from datetime import datetime
from io import BytesIO
from os import getcwd, path
from pathlib import Path
from typing import List

import httpx
import pandas as pd
from PIL import Image

from domain import Article
from locallogger import logger


class ExporterService:
    def __init__(self, articles: List[Article]):
        self.articles = articles
        self.excel_path = path.join(
            getcwd(),
            "output",
            "excel",
            datetime.today().strftime("%Y-%m-%d-%H:%M:%S.xls"),
        )
        Path(self.excel_path).parent.mkdir(parents=True, exist_ok=True)

    def execute(self):
        for article in self.articles:
            self.download_image(article)

        self.generate_excel_from_articles(self.articles, self.excel_path)

    def download_image(self, article: Article) -> None:
        logger.info(f"Download image {article.img_url}")
        response = httpx.get(article.img_url)
        response.raise_for_status()
        file_path = self.get_image_path(article=article, content=response.content)
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as file:
            logger.info(f"Create image file {file_path}")
            file.write(response.content)

    @staticmethod
    def generate_excel_from_articles(articles: List[Article], file_path: str) -> None:
        data = [
            {
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "picture_filename": article.image_hash,
                "date": article.date,
                "total_query_occour": article.total_query_occour,
                "has_money_str": article.has_money_str,
            }
            for article in articles
        ]

        df = pd.DataFrame(data)

        df.to_excel(file_path, index=False, engine="openpyxl")

        logger.info(f"Excel file created: {file_path}")

    @staticmethod
    def get_image_path(article: Article, content: bytes) -> str:
        img_data = BytesIO(content)
        img = Image.open(img_data)
        img_format = img.format.lower()
        file_extension = img_format if img_format else "png"

        return path.join(
            getcwd(), "output", "images", f"{article.image_hash}.{file_extension}"
        )
