import hashlib
import re
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional, Tuple


@dataclass
class Article:
    search_query: str
    title: str
    description: str
    url: str
    img_url: Optional[str] = None
    _hash: str = field(init=False, repr=False)
    _image_hash: str = field(init=False, repr=False)
    date: date = field(default_factory=date.today())

    def __post_init__(self):
        if self.date is None:
            self.date = date.today()

        self._hash = self._compute_hash()
        self._image_hash = self._compute_image_hash()

    def _compute_hash(self) -> str:
        hash_func = hashlib.sha256()
        hash_func.update(self.url.encode("utf-8"))
        return hash_func.hexdigest()

    def _compute_image_hash(self) -> str:
        hash_func = hashlib.sha256()
        hash_func.update(self.img_url.encode("utf-8"))
        return hash_func.hexdigest()

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def image_hash(self) -> str:
        return self._image_hash

    @property
    def count_query_occour(self) -> str:
        return self.description.lower().count(
            self.search_query.lower()
        ) + self.title.lower().count(self.search_query.lower())

    @property
    def has_money_str(self) -> bool:
        pattern = r"(\$[\d.,]+)|([\d.,]+\s+dollars)|([\d.,]+\s+USD)"
        for text in [self.title, self.description]:
            if re.search(pattern, text):
                return True
        return False

    def __hash__(self) -> int:
        return int(self._hash, 16)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Article):
            return NotImplemented
        return self.hash == other.hash


def valid_months_in_ratio(date=date.today(), ratio=0):
    start_month = date.month - ratio
    start_year = date.year
    if start_month <= 0:
        start_year -= (abs(start_month) // 12) + 1
        start_month = 12 + (start_month % 12)

    valid_months = []
    for i in range(ratio + 1):
        month = (date.month - i) % 12
        year = date.year - (date.month - i) // 12
        valid_months.append((year, month))

    return valid_months


def filter_articles_by_valid_months(
    articles: List[Article], valid_months: Tuple[int, int]
) -> List[Article]:
    filtered_data = []
    for item in articles:
        if (item.date.year, item.date.month) in valid_months:
            filtered_data.append(item)

    return filtered_data
