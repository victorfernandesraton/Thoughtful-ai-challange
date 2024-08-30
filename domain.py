from dataclasses import dataclass, field
from datetime import date


@dataclass
class Article:
    title: str
    content: str
    url: str
    date: date = field(default_factory=date.today())

    def __post_init__(self):
        if self.date is None:
            self.date = date.today()
