# Twitter (X) community notes

Proposed [Twitter (X) community notes](https://x.com/i/communitynotes/download-data) from the last week, updated regularly. _[More…](#how-it-works)_

https://andylolz.github.io/x-community-notes/

## How it works

Community note data is fetched regularly [from Twitter (X)](https://x.com/i/communitynotes/download-data).

This data is always a couple of days old.

Notes are excluded if they meet any of the following criteria:

* Created more than a week ago
* Classifying the post as ‘not misleading’ (i.e. in support of the post)
* Currently rated ‘unhelpful’

We also attempt to filter out notes for deleted tweets and non-English tweets.

## Running locally

Initial setup:

```shell
# Install python dependencies
poetry install

# Install ruby dependencies (Jekyll)
bundle install

# Copy template .env.example into place (and populate)
cp .env.example .env
```

If you just need some notes data:

```shell
curl -o output/data/notes.json https://andylolz.github.io/x-community-notes/data/notes.json
```

Then to run:

```shell
# Start the development server
jekyll s -s output
```

If you want to download the notes yourself with python:
```
# Fetch notes
poetry run python -m x_notes

# Fetch a big list of GE2024 candidate twitter handles
poetry run python -m x_notes.fetch_candidates

# Optional: fetch tweets
poetry run python -m x_notes.fetch_tweets

```
