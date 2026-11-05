import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PATH = "data/philosophy.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def figure_to_dict(conn, row):
    """Turn a figure row into a dict and attach its tags."""
    figure = dict(row)
    tag_rows = conn.execute(
        "SELECT tag FROM tags WHERE figure_id = ?", (figure["id"],)
    ).fetchall()
    figure["tags"] = [t["tag"] for t in tag_rows]
    return figure


@app.route("/")
def home():
    return "Thorfinn's philosophy API is running."


@app.route("/api/schools")
def list_schools():
    conn = get_db()
    rows = conn.execute("SELECT * FROM schools ORDER BY name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/figures")
def list_figures():
    # Optional filters: /api/figures?school=...&world=...&tag=...
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
        conn.close()
        return jsonify({"error": "Figure not found"}), 404

    result = figure_to_dict(conn, row)
    conn.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)