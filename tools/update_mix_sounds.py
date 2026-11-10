"""Refresh the sound id -> name map in mix/index.html from the app's catalog.

Run after sounds are added to or renamed in the app:

    python tools/update_mix_sounds.py [path/to/catalog.json]

The catalog path defaults to ../sleep/SleepAid/Resources/Catalog/catalog.json,
the app repo checked out next to this one.
"""
import json
import re
import sys
from pathlib import Path

site = Path(__file__).resolve().parent.parent
catalog = Path(sys.argv[1]) if len(sys.argv) > 1 else site.parent / "sleep/SleepAid/Resources/Catalog/catalog.json"
page = site / "mix/index.html"

sounds = {s["id"]: s["name"] for s in json.loads(catalog.read_text(encoding="utf-8"))}
lines = ",\n".join(f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in sounds.items())
block = f"/* sounds:start */\nconst SOUNDS = {{\n{lines}\n}};\n/* sounds:end */"

html = page.read_text(encoding="utf-8")
updated, count = re.subn(r"/\* sounds:start \*/.*?/\* sounds:end \*/", lambda _: block, html, flags=re.S)
if count != 1:
    sys.exit("mix/index.html has no sounds:start/sounds:end block")
page.write_text(updated, encoding="utf-8", newline="\n")
print(f"{len(sounds)} sounds written to {page.relative_to(site)}")
