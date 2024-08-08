---
title: How it works
---

Community note data is fetched regularly [from Twitter (X)](https://x.com/i/communitynotes/download-data).

This data is always a couple of days old (**most recent data is from <time class="dt" datetime="{{ site.data.meta.most_recent }}" title="{{ site.data.meta.most_recent | date_to_rfc822 }}">{{ site.data.meta.most_recent }}</time>, scraped <time class="dt" datetime="{{ site.data.meta.scraped_at }}" title="{{ site.data.meta.scraped_at | date_to_rfc822 }}">{{ site.data.meta.scraped_at }}</time>**).

Notes are excluded if they meet any of the following criteria:

* Created more than a week ago
* Classifying the post as ‘not misleading’ (i.e. in support of the post)
* Currently rated ‘unhelpful’

We also attempt to filter out notes for deleted tweets and non-English tweets.

---

### Filter by author group

With thanks to [@leobenedictus](https://x.com/leobenedictus) for the suggestion, community notes can be filtered by current UK MPs.

---

### Special Twitter (X) language codes

When Twitter (X) can’t determine the language of a tweet, it uses one of several reserved language codes. For the purpose of language filtering, we’ve grouped these all together. But this is the breakdown:

|---------------|---------------------------------------------|
| Language code | Description                                 |
|---------------|---------------------------------------------|
| `art`         | Tweet contains emojis only                  |
| `qam`         | Tweet contains mentions only                |
| `qct`         | Tweet contains cashtags only                |
| `qht`         | Tweet contains hashtags only                |
| `qme`         | Tweet contains media only                   |
| `qst`         | Tweet text is very short                    |
| `und`         | Undefined (couldn’t determine the language) |
| `zxx`         | Tweet contains media or twitter card only   |
{: .table .table-striped .w-inherit }

---

### Tweet indexing status

After fetching new proposed community notes, the text of the tweets that the notes reference is not immediately searchable. In order to make it searchable, we need to fetch these tweets – a process that can take several hours. You can see the current status below.

{% if site.data.meta.total_tweets > 0 %}
  {% assign perc_fetched = site.data.meta.total_fetched | times: 100 | divided_by: site.data.meta.total_tweets %}
{% else %}
  {% assign perc_fetched = 0 %}
{% endif %}

<div class="progress my-2" style="max-width: 500px;" role="progressbar">
  <div class="progress-bar text-bg-{% if perc_fetched == 100 %}success{% elsif perc_fetched < 50 %}danger{% else %}warning{% endif %}" style="width: {{ perc_fetched }}%">{{ perc_fetched }}% ({% include commify.html number=site.data.meta.total_fetched %} / {% include commify.html number=site.data.meta.total_tweets %})</div>
</div>
{{ perc_fetched }}% of tweets are searchable.

<script>
  const dts = document.getElementsByClassName('dt');
  for (var i = 0; i < dts.length; i++) {
    var dt = dts[i];
    dt.textContent = luxon.DateTime.fromISO(dt.textContent).toRelative();
  }
</script>

---

### Why is the language unknown for some tweets?

Until we’ve fetched a tweet, we don’t know its language. So ‘unknown language’ may mean we haven’t yet fetched that tweet. Once we’ve fetched it (in the next hour or so) we should know the tweet author, language and text.

‘Unknown language’ may also mean the tweet has been deleted. In this case, we have no way of determining the tweet author, language or text.
