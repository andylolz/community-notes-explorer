import re
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.parse import urlparse

from .exceptions import DataNotFoundException
from .helpers import to_isoformat
from .tsv import get_todays_data

url_re = re.compile(r"https?:\/\/[^\s]+")
one_week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).timestamp()


def urlize(inp: str) -> str:
    def format_url(match: re.Match) -> str:
        url = match.group()
        try:
            pr = urlparse(url)
        except ValueError:
            return url
        relative_url = pr._replace(scheme="", netloc="").geturl()
        if len(relative_url) > 15:
            abbrev_url = f"{pr.scheme}://{pr.netloc}{relative_url[:15]}…"
        else:
            abbrev_url = url
        return f'<a target="_blank" href="{url}">{abbrev_url}</a>'

    return url_re.sub(lambda match: format_url(match), inp)


reasons_lookup = {
    "misleadingFactualError": 1,
    "misleadingManipulatedMedia": 2,
    "misleadingMissingImportantContext": 3,
    "misleadingOther": 4,
    "misleadingOutdatedInformation": 5,
    "misleadingSatire": 6,
    "misleadingUnverifiedClaimAsFact": 7,
    # "notMisleadingClearlySatire": 8,
    # "notMisleadingFactuallyCorrect": 9,
    # "notMisleadingOther": 10,
    # "notMisleadingOutdatedButNotWhenWritten": 11,
    # "notMisleadingPersonalOpinion": 12,
}


def get_notes(notes: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    notes_by_tweet_id = {
        note["tweet_id"]: note for note in notes.values() if "dl" in note
    }
    notes = {
        k: v
        for k, v in notes.items()
        if datetime.fromisoformat(v["created_at"]).timestamp() >= one_week_ago
    }
    try:
        gen = get_todays_data("notes/notes")
    except DataNotFoundException:
        return notes

    for row in gen:
        note_id = row["noteId"]
        created_at = to_isoformat(row["createdAtMillis"])
        if float(row["createdAtMillis"]) / 1000 < one_week_ago:
            # ignore old notes
            continue
        if row["classification"] == "NOT_MISLEADING":
            # ignore "not misleading" notes
            if note_id in notes:
                del notes[note_id]
            continue
        reasons = [v for k, v in reasons_lookup.items() if bool(int(row[k]))]
        note = notes.get(note_id, {})
        note.update(
            {
                "tweet_id": row["tweetId"],
                "note_id": note_id,
                "reasons": reasons,
                "summary": urlize(row["summary"]),
                "created_at": created_at,
            }
        )
        if "dl" not in note and note["tweet_id"] in notes_by_tweet_id:
            tweet_note = notes_by_tweet_id[note["tweet_id"]]
            for k in [
                "dl",
                "deleted",
                "lang",
                "tweet",
                "tweet_created_at",
                "user",
                "user_id",
            ]:
                if k in tweet_note:
                    note[k] = tweet_note[k]
        notes[note_id] = note
    return notes
