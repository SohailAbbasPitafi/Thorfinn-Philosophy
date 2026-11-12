# Thorfinn's Philosophy Path

A web app where Thorfinn, from the final arc of *Vinland Saga*, guides you
through the ideas of Greek thinkers, modern philosophers and anime characters.
He greets you, comments on each figure in his own calm voice, talks with them,
and can point you to the figures whose ideas fit a situation you describe.

> This is a non-commercial fan project. *Vinland Saga* and the other anime
> series mentioned belong to their creators and publishers. I am not affiliated
> with them.

## Features

- 23 figures across three worlds (Anime, Greek, Modern) grouped into 7 schools
- Filter by world, school or tag
- A page per figure with its own colour theme, portrait, core idea, life lesson
  and Thorfinn's comment
- A scripted conversation between Thorfinn and each figure
- A Thorfinn mascot that introduces the site and reacts on each page
- "Tell Thorfinn your situation": type a situation and get the closest figures

## Tech stack

- Python and Flask (backend and routes)
- SQLite (data stored in three tables: schools, figures, tags)
- HTML, CSS and vanilla JavaScript (frontend)
- scikit-learn (TF-IDF and cosine similarity for the matching box)

## How to run

```
git clone <your-repo-url>
cd Thorfinn-Philosophy
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
python db_setup.py
python app.py
```

Then open http://127.0.0.1:5000/

`db_setup.py` builds the SQLite database from `data/figures.json`. The
database file is not committed, so run it once after cloning.

## How the matching works

1. Each figure becomes one text document: tags (counted twice), core idea,
   life lesson, Thorfinn's comment, school summary and conversation lines.
2. TF-IDF turns every document into a vector, giving more weight to words that
   are rare across figures.
3. The user's sentence is turned into a vector the same way.
4. Cosine similarity ranks the figures, and the top three are shown.
5. If the best score is too low, Thorfinn says he is not sure instead of
   guessing. Messages containing signs of self-harm get a supportive message
   pointing to real help instead of a philosophy match.

**Limitation:** TF-IDF matches words, not meaning, so a sentence that shares no
words with the dataset may match poorly. A future version could use sentence
embeddings or an LLM.

## Project structure

```
app.py              Flask app and routes
matcher.py          TF-IDF matching
db_setup.py         builds the SQLite database from the JSON data
check_data.py       validates figures.json and themes.json
test_db.py          sample queries
data/               figures.json, themes.json, dialogues.json
templates/          index.html, figure.html
static/             CSS, JavaScript and images
tools/              helper scripts (image resizing, dialogue conversion)
```

## About the content

The first drafts of the dataset and the dialogues were written with AI
assistance, and I am reviewing and rewriting them in my own words.
The philosophical summaries are simplified for a general audience.



## Credits and image note

All portraits and the Thorfinn mascot are AI-generated illustrations (created
with ChatGPT's image generation). They are not real portraits or photographs.
The anime characters and Thorfinn belong to their creators and publishers, and
these images are fan art used only in this non-commercial learning project. I
am not affiliated with the creators.

## Ideas for the future

- LLM-powered chat with each figure
- More figures and schools
- Better matching with sentence embeddings