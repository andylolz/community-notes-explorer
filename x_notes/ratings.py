from typing import Any

from .exceptions import DataNotFoundException
from .helpers import load_notes, save_notes
from .tsv import get_generator

helpfulness_score = {
    "HELPFUL": 2,
    "SOMEWHAT_HELPFUL": 1,
    "NOT_HELPFUL": -2,
}


def add_ratings(notes: dict[str, dict[str, Any]]) -> None:
    for note in notes.values():
        if "ratings" in note:
            del note["ratings"]
        if "score" in note:
            del note["score"]

    index = 0
    while True:
        try:
            gen = get_generator("noteRatings/ratings", index)
        except DataNotFoundException:
            break
        for row in gen:
            if row["noteId"] in notes:
                note = notes[row["noteId"]]
                if "ratings" not in note:
                    note["ratings"] = 0
                    note["score"] = 0
                note["ratings"] += 1
                note["score"] += helpfulness_score[row["helpfulnessLevel"]]
        index += 1
    save_notes(notes)


if __name__ == "__main__":
    notes = load_notes()
    add_ratings(notes)
