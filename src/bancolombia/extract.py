from dataclasses import dataclass
from datetime import datetime as dt
import re

from bs4 import BeautifulSoup

INFO_REGEX = re.compile(
    r"Bancolombia le informa (?P<tt>\w+) por \$(?P<amount>(\d|\.|,)+) en (?P<venue>.+) (?P<date>\d\d:\d\d. \d\d/\d\d/\d{4}) (?P<pm>.*). I",  # noqa: E501
)


@dataclass
class Transaction:
    date: dt
    amount: float
    venue: str
    payment_method: str
    transation_type: str

    @classmethod
    def from_text(cls, text):
        match = INFO_REGEX.search(text)
        info = match.groupdict()

        return cls(
            date=dt.strptime(info["date"], "%H:%M. %d/%m/%Y"),
            amount=float(info["amount"].replace(".", "").replace(",", ".")),
            venue=info["venue"],
            payment_method=info["pm"],
            transation_type=info["tt"],
        )


def extract_transactions_from_soup(soup: BeautifulSoup) -> Transaction:
    for line in soup.text.split("\t"):
        if not line:
            continue

        if "Bancolombia le informa" in line:
            return Transaction.from_text(line)
