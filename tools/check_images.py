import json
import os
import unicodedata

def slugify(name):
    name = name.replace("ø", "o").replace("Ø", "O")
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return "-".join(name.lower().replace("-", " ").split())

with open("data/figures.json", encoding="utf-8") as f:
    figures = json.load(f)["figures"]

exts = ("jpg", "jpeg", "png", "webp", "svg")
missing = []
for fig in figures:
    slug = slugify(fig["name"])
    found = any(os.path.exists(f"static/img/{slug}.{e}") for e in exts)
    print(("OK       " if found else "MISSING  ") + slug)
    if not found:
        missing.append(slug)

print(f"\n{len(figures) - len(missing)} of {len(figures)} have images")