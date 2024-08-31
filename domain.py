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
    date: date = field(default_factory=date.today())
    total_query_occour: int = field(init=False)
    has_money_str: bool = field(init=False)

    def __post_init__(self):
        if self.date is None:
            self.date = date.today()

        self.total_query_occour = self.description.lower().count(
            self.search_query.lower()
        ) + self.title.lower().count(self.search_query.lower())
        self.has_money_str = self.__count_money_occurrences(
            self.title + self.description
        )

    def __hash__(self):
        # Use unique_id for hashing
        return hash(self.url)

    def __eq__(self, other):
        # Define equality based on unique_id
        if isinstance(other, Article):
            return self.url == other.url
        return False

    def __count_money_occurrences(self, combined_text) -> int:
        """
        Count occurrences of monetary values in both texts.
        Monetary formats handled:
        - $11.1
        - $111,111.11
        - 11 dollars
        - 11 USD
        """
        money_pattern = (
            r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+\.?\d*\s?(?:dollars|USD|usd)?"
        )

        matches = re.findall(money_pattern, combined_text, re.IGNORECASE)

        return bool(matches)


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
