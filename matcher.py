import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Matcher:
    def __init__(self, db_path, dialogues):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT figures.id, figures.name, figures.world,
                   schools.name AS school, schools.summary,
                   figures.core_idea, figures.life_lesson,
                   figures.thorfinn_comment
            FROM figures
            JOIN schools ON figures.school_id = schools.id
        """).fetchall()

        tags = {}
        for r in conn.execute("SELECT figure_id, tag FROM tags").fetchall():
            tags.setdefault(r["figure_id"], []).append(r["tag"])
        conn.close()

        self.figures = []
        documents = []
        for r in rows:
            fig = dict(r)
            tag_text = " ".join(tags.get(fig["id"], []))
            convo = " ".join(line["text"] for line in dialogues.get(fig["name"], []))
            # tags appear twice so they carry more weight
            doc = " ".join([
                tag_text, tag_text,
                fig["core_idea"], fig["life_lesson"],
                fig["thorfinn_comment"], fig["summary"], convo,
            ])
            self.figures.append(fig)
            documents.append(doc)

        self.vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform(documents)

    def match(self, text, n=3):
        query = self.vectorizer.transform([text])
        scores = cosine_similarity(query, self.matrix)[0]
        best = scores.argsort()[::-1][:n]
        return [
            {**self.figures[i], "score": float(scores[i])}
            for i in best
            if scores[i] > 0
        ]