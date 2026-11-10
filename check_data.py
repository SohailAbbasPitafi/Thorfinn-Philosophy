import json

with open("data/figures.json", encoding="utf-8") as f:
    data = json.load(f)

school_names = {s["name"] for s in data["schools"]}

for fig in data["figures"]:
    if fig["school"] not in school_names:
        print("Unknown school:", fig["name"], "->", fig["school"])
    if fig["world"] not in ("Anime", "Greek", "Modern"):
        print("Bad world:", fig["name"], "->", fig["world"])

with open("data/themes.json", encoding="utf-8") as f:
    themes = json.load(f)

for fig in data["figures"]:
    if fig["name"] not in themes:
        print("No theme for:", fig["name"])
        
print(len(data["schools"]), "schools,", len(data["figures"]), "figures")