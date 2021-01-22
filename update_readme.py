import pathlib
import feedparser
import re


def fetch_writing():
    entries = feedparser.parse(
        'https://jckling.github.io/atom.xml')['entries'][:5]
    return [
        {
            'title': entry['title'],
            'url': entry['link'].split('#')[0],
            'published': entry['published'].split('T')[0]
        }
        for entry in entries
    ]


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        r'<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->'.format(marker, marker),
        re.DOTALL,
    )
    if not inline:
        chunk = '\n{}\n'.format(chunk)
    chunk = '<!-- {} starts -->{}<!-- {} ends -->'.format(
        marker, chunk, marker)
    return r.sub(chunk, content)


if __name__ == '__main__':
    root = pathlib.Path(__file__).parent.resolve()
    readme_path = root / 'README.md'
    readme = readme_path.open(encoding='UTF-8').read()

    entries = fetch_writing()[:5]
    entries_md = '\n'.join(
        ['- [{title}]({url}) ({published})'.format(**entry)
         for entry in entries]
    )

    rewritten = replace_chunk(readme, 'blog', entries_md)
    readme_path.open('w', encoding='UTF-8').write(rewritten)
