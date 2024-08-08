import json
from datetime import datetime, timedelta, timezone
from io import BytesIO

import requests

MAX_AGE_IN_DAYS = 3


def health_check() -> None:
    r = requests.get(
        "https://github.com/andylolz/x-community-notes/raw/gh-pages/_data/meta.json"
    )
    meta = json.load(BytesIO(r.content))
    delta = datetime.now(timezone.utc) - datetime.fromisoformat(meta["most_recent"])

    if delta > timedelta(days=MAX_AGE_IN_DAYS):
        raise Exception(f"Most recent tweet is more than {MAX_AGE_IN_DAYS} days old.")


if __name__ == "__main__":
    health_check()
