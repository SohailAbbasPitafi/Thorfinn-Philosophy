import os
import json
import sqlite3
import unicodedata
from flask import Flask, jsonify, request, render_template, abort

app = Flask(__name__)

DB_PATH = "data/philosophy.db"
THEMES_PATH = "data/themes.json"
IMAGE_EXTENSIONS = ("jpg", "jpeg", "png", "webp", "svg")

with open(THEMES_PATH, encoding="utf-8") as f:
    THEMES = json.load(f)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def slugify(name):
    """'Søren Kierkegaard' -> 'soren-kierkegaard'"""
    name = name.replace("ø", "o").replace("Ø", "O")
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return "-".join(name.lower().replace("-", " ").split())


def find_image(name):
    """Return the URL of static/img/<slug>.<ext> if it exists, else None."""
    slug = slugify(name)
    for ext in IMAGE_EXTENSIONS:
        path = os.path.join(app.static_folder, "img", f"{slug}.{ext}")
        if os.path.exists(path):
            return f"/static/img/{slug}.{ext}"
    return None


def make_initials(name):
    words = name.split()
    if len(words) == 1:
        return words[0][0].upper()
    return (words[0][0] + words[-1][0]).upper()


def figure_to_dict(conn, row):
    """Turn a figure row into a dict with tags, theme and image."""
    figure = dict(row)
    tag_rows = conn.execute(
        "SELECT tag FROM tags WHERE figure_id = ?", (figure["id"],)
    ).fetchall()
    figure["tags"] = [t["tag"] for t in tag_rows]
    figure["theme"] = THEMES.get(figure["name"], THEMES["_thorfinn"])
    figure["image"] = find_image(figure["name"])
    figure["initials"] = make_initials(figure["name"])
    return figure


def fetch_figure(conn, figure_id):
    row = conn.execute(
        """
        SELECT figures.*, schools.name AS school, schools.thorfinn_intro
        FROM figures
        JOIN schools ON figures.school_id = schools.id
        WHERE figures.id = ?
        """,
        (figure_id,),
    ).fetchone()
    if row is None:
        return None
    return figure_to_dict(conn, row)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/figure/<int:figure_id>")
def figure_page(figure_id):
    conn = get_db()
    figure = fetch_figure(conn, figure_id)
    conn.close()
    if figure is None:
        abort(404)
    return render_template("figure.html", figure=figure, thorfinn=THEMES["_thorfinn"])


@app.route("/api/schools")
def list_schools():
    conn = get_db()
    rows = conn.execute("SELECT * FROM schools ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/figures")
def list_figures():
    school = request.args.get("school")
    world = request.args.get("world")
    tag = request.args.get("tag")

    query = """
        SELECT figures.*, schools.name AS school
        FROM figures
        JOIN schools ON figures.school_id = schools.id
        WHERE 1=1
    """
    params = []

    if school:
        query += " AND schools.name = ?"
        params.append(school)
    if world:
        query += " AND figures.world = ?"
        params.append(world)
    if tag:
        query += " AND figures.id IN (SELECT figure_id FROM tags WHERE tag = ?)"
        params.append(tag)

    query += " ORDER BY figures.name"

    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    result = [figure_to_dict(conn, r) for r in rows]
    conn.close()
    return jsonify(result)


@app.route("/api/figures/<int:figure_id>")
def get_figure(figure_id):
    conn = get_db()
    figure = fetch_figure(conn, figure_id)
    conn.close()
    if figure is None:
        return jsonify({"error": "Figure not found"}), 404
    return jsonify(figure)


if __name__ == "__main__":
    app.run(debug=True)