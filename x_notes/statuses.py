from typing import Any

from .exceptions import DataNotFoundException
from .helpers import to_isoformat
from .tsv import get_generator

helpful = "CURRENTLY_RATED_HELPFUL"
unhelpful = "CURRENTLY_RATED_NOT_HELPFUL"


def add_statuses(notes: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    try:
        gen = get_generator("noteStatusHistory/noteStatusHistory")
    except DataNotFoundException:
        return notes

    for row in gen:
        note_id = row["noteId"]
        if note_id not in notes:
            continue
        if row["currentStatus"] == unhelpful:
            # this is currently rated unhelpful,
            # so we’ll exclude it
            del notes[note_id]
            continue
        if (
            row["firstNonNMRStatus"] != helpful
            and row["mostRecentNonNMRStatus"] != helpful
        ):
            # no status update here, so move on
            continue
        if row["firstNonNMRStatus"] == helpful:
            from_ts = to_isoformat(row["timestampMillisOfFirstNonNMRStatus"])
        else:
            from_ts = to_isoformat(row["timestampMillisOfLatestNonNMRStatus"])
        notes[note_id]["shown"] = from_ts
        if row["currentStatus"] != helpful:
            # the current timestamp often doesn’t appear to be useful.
            # I suspect because there are cases where the status
            # is disputed, so the current status changes frequently
            notes[note_id]["removed"] = to_isoformat(
                row["timestampMillisOfCurrentStatus"]
            )
    return notes
