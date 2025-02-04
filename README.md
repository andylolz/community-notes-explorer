# Community notes explorer

[![Health check](https://github.com/andylolz/community-notes-explorer/actions/workflows/health_check.yml/badge.svg)](https://github.com/andylolz/community-notes-explorer/actions/workflows/health_check.yml)

Proposed [Twitter (X) community notes](https://x.com/i/communitynotes/download-data) from the last week, updated regularly. _[More…](#how-it-works)_

https://communitynotesexplorer.com

## How it works

Community note data is fetched regularly [from Twitter (X)](https://x.com/i/communitynotes/download-data).

This data is always a couple of days old.

Notes are excluded if they meet any of the following criteria:

* Created more than a week ago
* Classifying the post as ‘not misleading’ (i.e. in support of the post)
* Currently rated ‘unhelpful’

We also attempt to filter out notes for deleted posts and non-English posts.

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

If you just need some notes data and metadata:

```shell
curl -L -o output/data/notes.json https://github.com/andylolz/community-notes-explorer/raw/gh-pages/data/notes.json
curl -L -o output/_data/meta.json https://github.com/andylolz/community-notes-explorer/raw/gh-pages/_data/meta.json
```

Then to run:

```shell
# Start the development server
bundle exec jekyll s -s output
```

If you want to download the notes yourself with python:
```shell
# Fetch notes
poetry run python -m x_notes

# Optional: fetch posts
poetry run python -m x_notes.fetch_tweets
```
