from datetime import datetime, timedelta
from random import randint
from typing import Any

import requests
from loguru import logger

from .helpers import get_tweets_with_multi_notes, load_notes, save_notes
from .meta import update_meta


def get_next_unfetched_note(notes: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    return next((note for note in notes.values() if "dl" not in note), None)


def fetch_tweets() -> None:
    notes = load_notes()
    if not get_next_unfetched_note(notes):
        logger.info("No tweets to fetch")
        return

    tweets_with_multi_notes = get_tweets_with_multi_notes(notes)

    total_fetched = 0
    start_time = datetime.now()
    while True:
        if datetime.now() - start_time > timedelta(minutes=20):
            # 20 minutes is plenty. Give up for now
            break
        note = get_next_unfetched_note(notes)
        if not note:
            logger.info("No more tweets to fetch")
            break
        note_id = note["note_id"]
        note_update = {}
        try:
            tweet = requests.get(
                "https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&token={random_token}".format(
                    tweet_id=int(note["tweet_id"]),
                    random_token=randint(1_000_000, 10_000_000),
                )
            ).json()
        except Exception:
            print("Problem fetching tweet with ID " + note["tweet_id"])
        else:
            total_fetched += 1
            if "tombstone" not in tweet:
                try:
                    note_update["lang"] = tweet["lang"]
                    note_update["user"] = tweet["user"]["screen_name"]
                    note_update["user_id"] = tweet["user"]["id_str"]
                    note_update["tweet"] = tweet["text"]
                    note_update["tweet_created_at"] = tweet["created_at"]
                except Exception:
                    print("Problem updating note with ID " + note["tweet_id"])
                    raise
            else:
                note_update["deleted"] = 1
        finally:
            note_update["dl"] = 1
            for update_note_id in tweets_with_multi_notes.get(
                note["tweet_id"], [note_id]
            ):
                notes[update_note_id] = {**notes[update_note_id], **note_update}

    update_meta(
        {
            "total_tweets": len({note["tweet_id"] for note in notes.values()}),
            "total_fetched": len(
                {note["tweet_id"] for note in notes.values() if "dl" in note}
            ),
        }
    )

    save_notes(notes)

    if total_fetched == 0:
        raise Exception("Failed to fetch any tweets")


if __name__ == "__main__":
    fetch_tweets()
