import json

RAW = "data/dialogues_raw.json"
OUT = "data/dialogues.json"
FIGURES = "data/figures.json"

with open(RAW, encoding="utf-8") as f:
    lines = json.load(f)

# Every conversation is Thorfinn + one figure. A Thorfinn line belongs to
# the next non-Thorfinn speaker after it.
grouped = {}
for i, line in enumerate(lines):
    if line["speaker"] != "Thorfinn":
        owner = line["speaker"]
    else:
        owner = None
        for later in lines[i + 1:]:
            if later["speaker"] != "Thorfinn":
                owner = later["speaker"]
                break
        if owner is None:
            print("Skipped a trailing Thorfinn line:", line["text"])
            continue
    grouped.setdefault(owner, []).append(
        {"speaker": line["speaker"], "text": line["text"]}
    )

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(grouped, f, indent=2, ensure_ascii=False)

with open(FIGURES, encoding="utf-8") as f:
    names = {fig["name"] for fig in json.load(f)["figures"]}

print(len(grouped), "conversations written")
print("Missing:", sorted(names - set(grouped)))
print("Wrong key:", sorted(set(grouped) - names))
for name, convo in grouped.items():
    print(f"  {name}: {len(convo)} lines")