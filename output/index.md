---
title: Community notes explorer
---

Proposed [Twitter (X) community notes](https://x.com/i/communitynotes/download-data) from the last week, updated regularly. _[More…]({{ '/about/' | relative_url }})_

<div class="table-responsive">
  <table id="notes-table" class="table table-striped" data-order='[[ 0, "desc" ]]'>
    <thead>
      <tr>
        <th>Created</th>
        <th>Tweet</th>
        <th>Note(s)</th>
        <th>Reason for note</th>
        <th>Tweet language</th>
        <th>Tweet status</th>
        <th>Tweet author</th>
        <th>Tweet content</th>
        <th>Max score</th>
      </tr>
    </thead>
    <tbody>
    </tbody>
  </table>
</div>

<script>
  const mps = {% if site.data.mps %}{{ site.data.mps | jsonify }}{% else %}[]{% endif %};

  /*
  This list comes from:
  https://developer.x.com/en/docs/twitter-api/enterprise/powertrack-api/guides/operators

  It’s mostly BCP-47, but with some idiosyncracies.
  E.g.:
    * Hebrew is `iw` instead of `he`
    * Indonesian is `in` instead of `id`
    * Haitian Creole is included (`ht`)
  */
  const langLookup = {'am': 'Amharic', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bo': 'Tibetan', 'bs': 'Bosnian', 'ca': 'Catalan', 'ckb': 'Sorani Kurdish', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'dv': 'Maldivian', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'eu': 'Basque', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi', 'hi-Latn': 'Latinized Hindi', 'hr': 'Croatian', 'ht': 'Haitian Creole', 'hu': 'Hungarian', 'hy': 'Armenian', 'in': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew', 'ja': 'Japanese', 'ka': 'Georgian', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'lo': 'Lao', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ml': 'Malayalam', 'mr': 'Marathi', 'my': 'Burmese', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'or': 'Oriya', 'pa': 'Panjabi', 'pl': 'Polish', 'ps': 'Pashto', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tl': 'Tagalog', 'tr': 'Turkish', 'ug': 'Uyghur', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh-CN': 'Simplified Chinese', 'zh-TW': 'Traditional Chinese', 'zh': 'Chinese', 'art': 'X', 'qam': 'X', 'qct': 'X', 'qht': 'X', 'qme': 'X', 'qst': 'X', 'und': 'X', 'zxx': 'X'}

  const reasonsLookup = {1: "Factual error", 2: "Manipulated media", 3: "Missing important context", 4: "Other", 5: "Outdated information", 6: "Satire", 7: "Unverified claim as fact"}

  const getReasons = function (values) {
    if (!Array.isArray(values)) {
      return values;
    }
    return values.map(v => reasonsLookup[v]).join(", ");
  }

  const includesReason = function (reason) {
    return function (rowData, rowIdx) {
      for (let i = 0; i < rowData['notes'].length; i++) {
        if (rowData['notes'][i]['reasons'].includes(reason)) {
          return true;
        }
      }
      return false;
    }
  }

  const showScore = function (score) {
    if (score === undefined) {
      score = 0;
    }
    return ' <small>[' + score + ']</small>';
  }

  let table = new DataTable('#notes-table', {
    layout: {
      top2Start: 'search',
      top: 'searchPanes',
      topStart: 'info',
      topEnd: 'paging',
      bottomStart: 'info',
      bottom2Start: 'pageLength'
    },
    fixedHeader: true,
    ajax: {
      url: '{{ '/data/notes.json' | relative_url }}',
      dataSrc: ''
    },
    columns: [
      {
        data: 'tweet_created_at',
        defaultContent: '',
        render: function (data, type, row, meta) {
          if (type !== 'display') {
            return data;
          }
          if (data) {
            dt = luxon.DateTime.fromISO(data).toFormat('d MMM yyyy');
          } else {
            dt = 'Unknown';
          }
          return '<a href="https://x.com/i/birdwatch/t/' + row['tweet_id'] + '" target="_blank">' + dt + '</a>';
        },
        searchable: false
      },
      {
        data: 'tweet_id',
        width: '550px',
        render: function (data, type, row, meta) {
          if (type !== 'display') {
            return data;
          }
          content = row['tweet'] ? row['tweet'] : '';
          return '<blockquote class="twitter-tweet">' + content + '<a href="https://twitter.com/_/status/' + data + '"></a></blockquote>';
        }
      },
      {
        data: 'notes',
        render: function (data, type, row, meta) {
          let output = data[0]['summary'] + showScore(data[0]['score']);
          for (let i = 1; i < data.length; i++) {
            output = output + '<br><hr>' + data[i]['summary'] + showScore(data[i]['score']);
          }
          return output;
        }
      },
      {
        data: 'notes',
        visible: false,
        searchPanes: {
          options: [
            {
              label: 'Factual error',
              value: includesReason(1),
            },
            {
              label: 'Manipulated media',
              value: includesReason(2),
            },
            {
              label: 'Missing important context',
              value: includesReason(3),
            },
            {
              label: 'Other',
              value: includesReason(4),
            },
            {
              label: 'Outdated information',
              value: includesReason(5),
            },
            {
              label: 'Satire',
              value: includesReason(6),
            },
            {
              label: 'Unverified claim as fact',
              value: includesReason(7),
            }
          ]
        }
      },
      {
        data: 'lang',
        visible: false,
        defaultContent: '',
        render: function (data, type, row, meta) {
          if (!data) {
            if (type === 'sort') {
              return '~ (put this last)';
            }
            if (type === 'display') {
              return 'Unknown language (see about page)';
            }
            return data;
          }
          const niceName = langLookup[data];
          if (niceName === 'X') {
            // there are a handful of language codes that are used for
            // esoteric Twitter (X) things, including emoji-only tweets (`art`)
            // and hashtag-only tweets (`qht`). We lump these all together
            if (type === 'display') {
              return 'Twitter (X) special (see about page)';
            }
            return niceName;
          }
          if (type === 'display' || type === 'sort') {
            return niceName;
          }
          return data;
        }
      },
      {
        data: 'deleted',
        visible: false,
        defaultContent: 0,
        render: function (data, type, row, meta) {
          if (type === 'display') {
            return (data === 1) ? 'Deleted' : 'Published';
          }
          return data;
        }
      },
      {
        data: 'user',
        searchable: true,
        visible: false,
        defaultContent: '',
        searchPanes: {
          threshold: 1,
          options: [
            {
              label: 'UK MPs',
              value: function (rowData, rowIdx) {
                if (!rowData['user']) {
                  return false;
                }
                return mps.includes(rowData['user_id']);
              }
            }
          ]
        }
      },
      {
        data: 'tweet',
        searchable: true,
        visible: false,
        defaultContent: ''
      },
      {
        data: 'notes',
        searchable: false,
        visible: true,
        defaultContent: 0,
        render: function (data, type, row, meta) {
          return data[0]['score'];
        }
      }
    ],
    drawCallback: function (settings) {
      twttr.widgets.load();
    },
    searchPanes: {
      orderable: false,
      columns: [4, 5, 6, 3],
      preSelect: [
        {
          column: 4,
          rows: ['en', 'X', '']
        },
        {
          column: 5,
          rows: [0]
        },
      ],
      initCollapsed: true
    }
  });

  twttr.events.bind(
    'rendered',
    function () {
      table.fixedHeader.adjust();
    }
  );
</script>
