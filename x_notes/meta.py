import json
from datetime import UTC, datetime
from typing import Any


def load_meta() -> dict[str, Any]:
    with open("output/_data/meta.json") as fh:
        return json.load(fh)


def account_locked_until() -> str | None:
    meta = load_meta()
    if not meta.get("locked_until"):
        return None
    if datetime.fromisoformat(meta["locked_until"]) < datetime.now(UTC):
        return None
    return meta["locked_until"]


def save_meta(meta: dict[str, Any]) -> None:
    with open("output/_data/meta.json", "w") as fh:
        json.dump(meta, fh)


def update_meta(update: dict[str, Any]) -> None:
    meta = load_meta()
    meta = {**meta, **update}
    save_meta(meta)


def update_meta_from_notes(notes: dict[str, dict[str, Any]]) -> None:
    update = {
        "scraped_at": datetime.now(UTC).isoformat(),
        "total_tweets": len({note["tweet_id"] for note in notes.values()}),
        "total_fetched": len(
            {note["tweet_id"] for note in notes.values() if "dl" in note}
        ),
    }

    if update["total_tweets"]:
        update["most_recent"] = list(notes.values())[0]["created_at"]

    update_meta(update)
