import json
from os import environ
from typing import Any
from twscrape import API, NoAccountError
from .github import update_secret
from .helpers import load_notes, save_notes


async def login() -> API:
    print("Attempting to log in")
    api = API()

    username = environ["USER"]
    account_kwargs = {
        "username": username,
        "password": environ["PASS"],
        "email": environ["EMAIL"],
        "email_password": "",
    }
    proxy = environ.get("PROXY")
    if proxy:
        account_kwargs["proxy"] = proxy
    cookies = environ.get("COOKIES")
    if cookies:
        account_kwargs["cookies"] = cookies

    await api.pool.add_account(**account_kwargs)
    if not cookies:
        await api.pool.login_all()
        account = await api.pool.get(username)
        if environ.get("UPDATE_SECRET"):
            print("Updating secret ...")
            update_secret("COOKIES", json.dumps(account.cookies))
    return api


async def fetch_tweets() -> None:
    def get_next_unfetched_note(notes: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
        return next((note for note in notes.values() if "dl" not in note), None)

    notes = load_notes()
    if not get_next_unfetched_note(notes):
        print("No tweets to fetch")
        return

    api = await login()

    while True:
        note = get_next_unfetched_note(notes)
        if not note:
            print("No more tweets to fetch")
            break
        note_id = note["note_id"]
        try:
            tweet = await api.tweet_details(int(note["tweet_id"]))
        except NoAccountError:
            print("Rate limited – giving up")
            break
        account = await api.pool.get(environ["USER"])
        if not account.active:
            print("Failed to fetch tweet")
            if environ.get("COOKIES"):
                await api.pool.delete_inactive()
                del environ["COOKIES"]
                api = await login()
            continue
        note["dl"] = 1
        if tweet:
            note["lang"] = tweet.lang
            note["user"] = tweet.user.username
            note["tweet"] = tweet.rawContent
        else:
            note["deleted"] = 1
        notes[note_id] = note

    save_notes(notes)
