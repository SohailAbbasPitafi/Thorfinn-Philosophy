import json
import sqlite3
import os

DB_PATH = "data/philosophy.db"
JSON_PATH = "data/figures.json"

# Start fresh every time so you never get duplicates
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    summary TEXT,
    thorfinn_intro TEXT
)
""")

cur.execute("""
CREATE TABLE figures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    world TEXT NOT NULL,
    school_id INTEGER NOT NULL,
    core_idea TEXT,
    life_lesson TEXT,
    thorfinn_comment TEXT,
    FOREIGN KEY (school_id) REFERENCES schools(id)
)
""")

cur.execute("""
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    figure_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (figure_id) REFERENCES figures(id)
)
""")

# Insert schools and remember their ids
school_ids = {}
for s in data["schools"]:
    cur.execute(
        "INSERT INTO schools (name, summary, thorfinn_intro) VALUES (?, ?, ?)",
        (s["name"], s["summary"], s["thorfinn_intro"]),
    )
    school_ids[s["name"]] = cur.lastrowid

# Insert figures and their tags
for fig in data["figures"]:
    cur.execute(
        """INSERT INTO figures
           (name, world, school_id, core_idea, life_lesson, thorfinn_comment)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            fig["name"],
            fig["world"],
            school_ids[fig["school"]],
            fig["core_idea"],
            fig["life_lesson"],
            fig["thorfinn_comment"],
        ),
    )
    figure_id = cur.lastrowid
    for tag in fig["tags"]:
        cur.execute(
            "INSERT INTO tags (figure_id, tag) VALUES (?, ?)", (figure_id, tag)
        )

conn.commit()

n_schools = cur.execute("SELECT COUNT(*) FROM schools").fetchone()[0]
n_figures = cur.execute("SELECT COUNT(*) FROM figures").fetchone()[0]
print(f"Database built: {n_schools} schools, {n_figures} figures")

conn.close()