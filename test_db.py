import sqlite3

conn = sqlite3.connect("data/philosophy.db")
cur = conn.cursor()

print("=== Figures grouped by school ===")
rows = cur.execute("""
    SELECT schools.name, figures.name, figures.world
    FROM figures
    JOIN schools ON figures.school_id = schools.id
    ORDER BY schools.name, figures.name
""").fetchall()

current_school = None
for school, figure, world in rows:
    if school != current_school:
        print(f"\n{school}")
        current_school = school
    print(f"  - {figure} ({world})")

print("\n=== Figures tagged 'freedom' ===")
rows = cur.execute("""
    SELECT figures.name
    FROM figures
    JOIN tags ON tags.figure_id = figures.id
    WHERE tags.tag = ?
""", ("freedom",)).fetchall()

for (name,) in rows:
    print("  -", name)

conn.close()