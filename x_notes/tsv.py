import datetime
from typing import Generator

import requests
from stream_unzip import stream_unzip

from .exceptions import DataNotFoundException


def zipped_chunks(url: str) -> Generator:
    # Iterable that yields the bytes of a zip file
    r = requests.get(url, stream=True)
    r.raise_for_status()
    yield from r.iter_content(chunk_size=65536)


def get_generator(fname: str, date: str, index: int = 0) -> Generator:
    url = f"https://ton.twimg.com/birdwatch-public-data/{date}/{fname}-{index:05d}.zip"
    zip_contents = stream_unzip(zipped_chunks(url))
    _, _, chunks = next(zip_contents)  # zips only contain one file

    def _data_generator(chunks) -> Generator:
        headers = None
        remainder = b""
        for chunk in chunks:
            data = remainder + chunk
            rows = data.split(b"\n")  # I don’t like this, but
            if not headers:
                headers = rows.pop(0).decode().split("\t")
            for row in rows[:-1]:
                yield dict(zip(headers, row.decode().split("\t")))
            remainder = rows[-1]
        if headers and remainder:
            yield dict(zip(headers, remainder.decode().split("\t")))

    return _data_generator(chunks)


def get_todays_data(fname: str, index: int = 0) -> Generator:
    num_days_ago_to_try = 5
    today = datetime.date.today()
    for n in range(num_days_ago_to_try + 1):
        try:
            n_days_ago = today - datetime.timedelta(days=n)
            return get_generator(fname, n_days_ago.strftime("%Y/%m/%d"), index)
        except Exception:
            pass
    raise DataNotFoundException
