---
title: How it works
---

Community note data is fetched regularly [from Twitter (X)](https://x.com/i/communitynotes/download-data).

This data is always a couple of days old (**most recent data is from <time class="dt" datetime="{{ site.data.meta.most_recent }}" title="{{ site.data.meta.most_recent | date_to_rfc822 }}">{{ site.data.meta.most_recent }}</time>, scraped <time class="dt" datetime="{{ site.data.meta.scraped_at }}" title="{{ site.data.meta.scraped_at | date_to_rfc822 }}">{{ site.data.meta.scraped_at }}</time>**).

Notes are excluded if they meet any of the following criteria:

* Created more than a week ago
* Classifying the post as ‘not misleading’ (i.e. in support of the post)
* Currently rated ‘unhelpful’

We also attempt to filter out notes for deleted posts and non-English posts.

---

### Filter by author group

With thanks to [@leobenedictus](https://x.com/leobenedictus) for the suggestion, community notes can be filtered by current UK MPs.

---

### Special Twitter (X) language codes

When Twitter (X) can’t determine the language of a post, it uses one of several reserved language codes. For the purpose of language filtering, we’ve grouped these all together. But this is the breakdown:

|---------------|---------------------------------------------|
| Language code | Description                                 |
|---------------|---------------------------------------------|
| `art`         | Post contains emojis only                   |
| `qam`         | Post contains mentions only                 |
| `qct`         | Post contains cashtags only                 |
| `qht`         | Post contains hashtags only                 |
| `qme`         | Post contains media only                    |
| `qst`         | Post text is very short                     |
| `und`         | Undefined (couldn’t determine the language) |
| `zxx`         | Post contains media or twitter card only    |
{: .table .table-striped .w-inherit }

---

### Post indexing status

After fetching new proposed community notes, the text of the posts that the notes reference is not immediately searchable. In order to make it searchable, we need to fetch these posts – a process that can take several hours. You can see the current status below.

{% if site.data.meta.total_tweets > 0 %}
  {% assign perc_fetched = site.data.meta.total_fetched | times: 100 | divided_by: site.data.meta.total_tweets %}
{% else %}
  {% assign perc_fetched = 0 %}
{% endif %}

<div class="progress my-2" style="max-width: 500px;" role="progressbar">
  <div class="progress-bar progress-bar-striped bg-{% if perc_fetched == 100 %}success{% elsif perc_fetched < 50 %}danger{% else %}warning{% endif %}" style="width: {{ perc_fetched }}%"></div>
</div>
{{ perc_fetched }}% of posts ({% include commify.html number=site.data.meta.total_fetched %} / {% include commify.html number=site.data.meta.total_tweets %}) are currently searchable.

<script>
  const dts = document.getElementsByClassName('dt');
  for (var i = 0; i < dts.length; i++) {
    var dt = dts[i];
    dt.textContent = luxon.DateTime.fromISO(dt.textContent).toRelative();
  }
</script>

---

### Why is the language unknown for some posts?

Until we’ve fetched a post, we don’t know its language. So ‘unknown language’ may mean we haven’t yet fetched that post. Once we’ve fetched it (in the next hour or so) we should know the post author, language and text.

‘Unknown language’ may also mean the post has been deleted. In this case, we have no way of determining the post author, language or text.
