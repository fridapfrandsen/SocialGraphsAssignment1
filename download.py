import re
from urllib.request import urlopen, Request
import urllib.parse
import json
import os

text = open("wiki")

pattern = re.compile(r"\[\[(?!File:|Image:|Category:|Template:)([^\]|#]+)(?:\|([^\]]+))?\]\]")

matches = pattern.findall(text.read())

# Funktion til at gøre filnavne sikre
def sanitize_filename(name):
    # Erstat problematiske tegn med underscore
    return re.sub(r'[\\/*?:"<>|]', "_", name)

titles = []
for title, display in matches:
    url_title = title.replace(" ", "_")
    titles.append(url_title)

headers = {"User-Agent": "FridaBot/0.1 (https://example.com; frida@example.com)"}

for title in titles:
    baseurl = "https://en.wikipedia.org/w/api.php?"
    action = "action=query"
    title_param = "titles=" + urllib.parse.quote(title)
    content = "prop=revisions&rvprop=content"
    dataformat = "format=json"

    url = "%s%s&%s&%s&%s" % (baseurl, action, title_param, content, dataformat)
    print(url)

    req = Request(url, headers=headers)

    response = urlopen(req)

    html = response.read()

    data = json.loads(html)

    pages = data["query"]["pages"]
    page = next(iter(pages.values()))

    if "revisions" in page:
        rev = page["revisions"][0]
    
        # Ny struktur (med slots)
        if "slots" in rev:
            wikitext = rev["slots"]["main"]["*"]
        # Ældre struktur uden slots
        elif "*" in rev:
            wikitext = rev["*"]
        else:
            print(f"Skipping {title}: revisions exist but no content")
            continue
    else:
        print(f"Skipping {title}: no revisions")
        continue
    
    safe_title = sanitize_filename(title)
    filename = os.path.join("wiki_pages", f"{safe_title}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(wikitext)
    
    print(f"Saved {title}")