from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Rank
import random

bp = Blueprint("main", __name__)

# Standardhintergründe (Fallback)
DEFAULT_BACKGROUNDS = {
    "Heer": "Hintergrund-Heer-Wald.png",
    "Luftwaffe": "Hintergrund-Luftwaffe-Grau.png",
    "Marine": "Hintergrund-Marine-Hell.png"
}

# Startseite
@bp.route("/")
def index():
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)

    # Den passenden Hintergrund für den aktuellen Branch holen
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    # Aktuellen Hintergrund merken (für andere Templates)
    if session.get("current_background") != background:
        session["current_background"] = background
        session.modified = True

    return render_template("index.html", background=background)

# Einstellungen
@bp.route("/settings", methods=["GET", "POST"])
def settings():
    defaults = {
        "default_branch": session.get("default_branch", "Heer"),
        "backgrounds": session.get("backgrounds", DEFAULT_BACKGROUNDS)
    }

    # Merke dir, von wo man kam
    next_page = request.args.get("next") or url_for("main.index")

    if request.method == "POST":
        branch_input = request.form.get("default_branch", "Heer").strip().capitalize()
        session["default_branch"] = branch_input

        backgrounds = {
            "Heer": request.form.get("bg_heer", defaults["backgrounds"]["Heer"]),
            "Luftwaffe": request.form.get("bg_luftwaffe", defaults["backgrounds"]["Luftwaffe"]),
            "Marine": request.form.get("bg_marine", defaults["backgrounds"]["Marine"])
        }

        session["backgrounds"] = backgrounds
        session.modified = True

        # Nach dem Speichern zur Ausgangsseite zurückkehren
        return redirect(request.form.get("next") or next_page)

    # GET: Seite anzeigen, mit verstecktem Feld für Rücksprung
    return render_template("settings.html", defaults=defaults, next_page=next_page)


# Tabelle (Dienstgrade)
@bp.route("/ranks")
def ranks():
    # Aktueller Truppenteil aus Query oder Session
    branch = request.args.get("branch", session.get("default_branch", "Heer"))
    user_backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)

    # Falls "Alle" gewählt wurde → Standardbranch verwenden
    if not branch or branch == "Alle":
        active_branch = session.get("default_branch", "Heer")
        background = user_backgrounds.get(active_branch, DEFAULT_BACKGROUNDS[active_branch])
        ranks = Rank.query.order_by(Rank.branch, Rank.sort_order).all()
    else:
        branch = branch.capitalize()
        background = user_backgrounds.get(branch, DEFAULT_BACKGROUNDS.get(branch))
        ranks = Rank.query.filter_by(branch=branch).order_by(Rank.sort_order).all()

    branches = ["Alle", "Heer", "Luftwaffe", "Marine"]

    # Hintergrund speichern für Template
    session["current_background"] = background

    return render_template(
        "ranks.html",
        ranks=ranks,
        branches=branches,
        selected_branch=branch or "Alle",
        background=background
    )

# Quiz (Modusauswahl)
@bp.route("/quizmodes")
def quizmodes():
    # Gewählten Branch aus Query oder Session holen
    branch = request.args.get("branch", session.get("default_branch", "Alle"))
    branches = ["Alle", "Heer", "Luftwaffe", "Marine"]

    # Branch speichern, damit Quiz-Routen ihn verwenden können
    session["quiz_branch"] = branch
    session.modified = True

    # Hintergrund (wie gehabt)
    background = session.get("current_background", "Hintergrund-Heer-Wald.png")

    return render_template(
        "quizmodes.html",
        background=background,
        branches=branches,
        selected_branch=branch
    )

# Quiz-Data (Hilfsfunktion)
def generate_quiz_data():
    # Aktueller Truppenteil aus Session (vom Filter auf /quizmodes)
    branch = session.get("quiz_branch", "Alle")

    # Dienstgrade laden – ggf. gefiltert
    if branch == "Alle":
        ranks = Rank.query.all()
    else:
        ranks = Rank.query.filter_by(branch=branch).all()

    # Fallback, falls kein Ergebnis
    if not ranks:
        ranks = Rank.query.all()

    # Wähle eine zufällige "richtige" Antwort
    correct = random.choice(ranks)

    # Wähle bis zu 3 falsche Optionen
    wrong = random.sample([r for r in ranks if r.id != correct.id], min(3, len(ranks) - 1))

    # Optionen mischen
    options = [correct] + wrong
    random.shuffle(options)

    # Hintergrund übernehmen
    background = session.get("current_background", DEFAULT_BACKGROUNDS["Heer"])

    return {
        "branch": branch,
        "background": background,
        "correct": correct,
        "options": options
    }

# Dienstgrad-Quiz (Text → Bild)
@bp.route("/quiz1")
def quiz1():
    data = generate_quiz_data()
    return render_template(
        "quiz1.html",
        correct=data["correct"],
        options=data["options"],
        background=data["background"],
        selected_branch=data["branch"]
    )


# Schulterklappen-Quiz (Bild → Text)
@bp.route("/quiz2")
def quiz2():
    data = generate_quiz_data()
    return render_template(
        "quiz2.html",
        correct=data["correct"],
        options=data["options"],
        background=data["background"],
        selected_branch=data["branch"]
    )

# Zeitmodus: Dienstgrad-Quiz
@bp.route("/quiz1_timer")
def quiz1_timer():
    ranks = Rank.query.all()

    # Wir bereiten eine saubere JSON-kompatible Struktur vor
    rank_data = []
    for r in ranks:
        rank_data.append({
            "id": r.id,
            "title": r.title or "",
            "abbreviation": r.abbreviation or "",
            "rank_group": r.rank_group or "",
            "rank_type": r.rank_type or "",
            "level_code": r.level_code or "",
            "description": r.description or "",
            "image_filename": r.image_filename or "",
            "branch": r.branch or ""
        })

    background = session.get("current_background", DEFAULT_BACKGROUNDS["Heer"])

    return render_template(
        "quiz1_timer.html",
        ranks=rank_data,
        background=background
    )

# Zeitmodus: Schulterklappen-Quiz
@bp.route("/quiz2_timer")
def quiz2_timer():
    data = generate_quiz_data()
    return render_template(
        "quiz2_timer.html",
        correct=data["correct"],
        options=data["options"],
        background=data["background"],
        selected_branch=data["branch"]
    )

# Karteikarten
@bp.route("/flashcards")
def flashcards():
    # Gewählten Branch aus Query-Param oder Session holen
    branch = request.args.get("branch", "Alle")

    # Basisabfrage
    query = Rank.query

    # Nur gefilterte Ränge, wenn Branch != Alle
    if branch != "Alle":
        query = query.filter_by(branch=branch)

    ranks = query.order_by(Rank.branch, Rank.sort_order).all()

    # Wenn keine Ergebnisse → Fallback
    if not ranks:
        ranks = Rank.query.order_by(Rank.sort_order).all()

    # Für JSON im Template vorbereiten
    rank_data = [
        {
            "id": r.id,
            "title": r.title,
            "abbreviation": r.abbreviation,
            "rank_group": r.rank_group,
            "rank_type": r.rank_type,
            "level_code": r.level_code,
            "description": r.description,
            "image_filename": r.image_filename,
            "branch": r.branch
        }
        for r in ranks
    ]

    # Hintergrund dynamisch
    background = session.get("current_background", "Hintergrund-Heer-Wald.png")

    return render_template(
        "flashcards.html",
        ranks=rank_data,
        background=background,
        selected_branch=branch
    )