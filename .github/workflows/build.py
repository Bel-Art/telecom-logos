""" builder """
from string import Template
import os
from os.path import getmtime, getsize, join
from datetime import datetime


def size(size_in_bytes):
    """convert"""
    size_kb = size_in_bytes / 1024.0
    size_mb = size_kb / 1024.0

    if size_mb >= 1:
        return f"{size_mb:.2f}M"
    elif size_kb >= 1:
        return f"{size_kb:.2f}K"
    return size_in_bytes


PATH_TO_TEMPLATE = ".github/workflows/index.html"
with open(PATH_TO_TEMPLATE, "r", encoding="utf-8") as template_file:
    html = template_file.read()

EXCLUDE_LIST = [".git", ".github", ".static"]
EXCLUDE_LIST_FULL = ["./README.md", "./.gitignore"]

CSS = """.thumbnail {
  position: relative;
  z-index: 0;
}

.thumbnail:hover {
  background-color: transparent;
  z-index: 50;
}

.thumbnail span {
  position: absolute;
  padding: 5px;
  left: -1000px;
  border: 1px dashed gray;
  visibility: hidden;
  color: black;
  text-decoration: none;
}

.thumbnail span > * {
  border-width: 0;
  padding: 2px;
  min-width: 800px;
}

.thumbnail:hover span {
  visibility: visible;
  top: 0;
  left: 60px; /*position where enlarged image should offset horizontally */
}"""

HEADER = """
"""

html = html.replace("<style></style>", f"{HEADER}<style>{CSS}</style>")

t = Template(
    """<tr>
    <td valign="top"><img src="$url" alt="[   ]" /></td>
    <td><a $add href="$file">$file $other</a></td>
    <td align="right">$date</td>
    <td align="right">$size</td>
    <td>&nbsp;</td>
</tr>"""
)

URL = "https://bel-art.github.io/telecom-logos"
REPO = "https://github.com/Bel-Art/telecom-logos"
LINK = f'<a href="{REPO}">{REPO}</a>'

UNKNOWN = f"{URL}/.static/unknown.gif"
FOLDER = f"{URL}/.static/folder.gif"


def create_index_html(folder):
    """create an index.html"""
    listed = sorted(os.listdir(folder))
    s = ""
    correct_html = f"{html}".replace(
        "<title></title>", f"<title>Index of {folder}</title>"
    )
    correct_html = correct_html.replace(
        "<h1></h1>",
        f"<h1>Index of {folder} - {LINK}</h1>",
    )
    for name in listed:
        if name == "index.html" or name in EXCLUDE_LIST:
            continue
        p = join(folder, name)
        if p in EXCLUDE_LIST_FULL:
            continue
        isdir = os.path.isdir(p)
        date = datetime.fromtimestamp(getmtime(p)).strftime("%Y-%m-%d %H:%M:%S")
        url = FOLDER if isdir else UNKNOWN
        preview = not isdir
        add = 'class="thumbnail"' if preview else ""
        other = ""
        if name.endswith(".md"):
            other = f'<span><iframe src="{name}"></iframe></span>'
        elif preview:
            other = f'<span><img src="{name}"></span>'
        s += t.substitute(
            file=name, date=date, size=size(getsize(p)), url=url, add=add, other=other
        )
        if isdir and name not in EXCLUDE_LIST:
            create_index_html(p)
    file_data = correct_html.replace("<placeholder></placeholder>", s)
    with open(join(folder, "index.html"), "w", encoding="utf-8") as file:
        file.write(file_data)


if __name__ == "__main__":
    create_index_html(".")
