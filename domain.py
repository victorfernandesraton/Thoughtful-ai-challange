import re
from dataclasses import dataclass, field
from datetime import date


@dataclass
class Article:
    search_query: str
    title: str
    description: str
    url: str
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
