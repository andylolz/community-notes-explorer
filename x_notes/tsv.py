import csv
import datetime
from io import StringIO
from typing import Generator

import requests

from .exceptions import DataNotFoundException


def get_generator(fname: str, date: datetime.date, index: int = 0) -> Generator:
    url_tmpl = (
        f"https://ton.twimg.com/birdwatch-public-data/{{date}}/{fname}-{index:05d}.tsv"
    )
    url = url_tmpl.format(date=date.strftime("%Y/%m/%d"))
    r = requests.get(url, stream=True)
    r.raise_for_status()

    def _data_generator() -> Generator:
        headers = None
        for line in r.iter_lines():
            cols = next(csv.reader(StringIO(line.decode()), delimiter="\t"))
            if not headers:
                headers = cols
                continue
            yield dict(zip(headers, cols))

    return _data_generator()


def get_todays_data(fname: str, index: int = 0) -> Generator:
    num_days_ago_to_try = 5
    today = datetime.date.today()
    for n in range(num_days_ago_to_try + 1):
        try:
            n_days_ago = today - datetime.timedelta(days=n)
            return get_generator(fname, n_days_ago, index)
        except Exception:
            pass
    raise DataNotFoundException
