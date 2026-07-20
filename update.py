# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "feedparser",
# ]
# ///
import re
from pathlib import Path

import feedparser

BLOG_FEED_URL = "https://jckling.github.io/atom.xml"


def fetch_writing() -> list[dict]:
    entries = feedparser.parse(BLOG_FEED_URL)["entries"][:5]
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": entry["published"].split("T")[0],
        }
        for entry in entries
    ]


def replace_chunk(content: str, marker: str, chunk: str) -> str:
    pattern = re.compile(
        rf"<!-- {marker} starts -->.*<!-- {marker} ends -->",
        re.DOTALL,
    )
    replacement = f"<!-- {marker} starts -->\n{chunk}\n<!-- {marker} ends -->"
    return pattern.sub(replacement, content)


def main() -> None:
    readme_path = Path(__file__).parent.resolve() / "README.md"

    with readme_path.open(encoding="utf-8") as f:
        readme = f.read()

    entries = fetch_writing()
    entries_md = "\n".join(
        f"- [{e['title']}]({e['url']}) ({e['published']})"
        for e in entries
    )

    rewritten = replace_chunk(readme, "blog", entries_md)

    with readme_path.open("w", encoding="utf-8") as f:
        f.write(rewritten)


if __name__ == "__main__":
    main()
