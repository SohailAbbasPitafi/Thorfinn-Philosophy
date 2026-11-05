import json

with open("data/figures.json", encoding="utf-8") as f:
    data = json.load(f)

school_names = {s["name"] for s in data["schools"]}

for fig in data["figures"]:
    if fig["school"] not in school_names:
        print("Unknown school:", fig["name"], "->", fig["school"])
    if fig["world"] not in ("Anime", "Greek", "Modern"):
        print("Bad world:", fig["name"], "->", fig["world"])

print(len(data["schools"]), "schools,", len(data["figures"]), "figures")