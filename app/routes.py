# =====================================
# IMPORTS
# =====================================
import random, csv, os
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import Rank, NATO


# =====================================
# BLUEPRINTS
# =====================================
# Haupt-Blueprint (Startseite, Einstellungen, generelle Logik)
bp_main = Blueprint("main", __name__)

# Separate Blueprints für Themenbereiche
bp_ranks = Blueprint("ranks", __name__, url_prefix="/ranks")
bp_nato = Blueprint("nato", __name__, url_prefix="/nato")


# =====================================
# STANDARDHINTERGRÜNDE
# =====================================
DEFAULT_BACKGROUNDS = {
    "Heer": "Hintergrund-Heer-Wald.png",
    "Luftwaffe": "Hintergrund-Luftwaffe-Grau.png",
    "Marine": "Hintergrund-Marine-Hell.png"
}


# =====================================
# STARTSEITE / LERNBEREICHE
# =====================================
@bp_main.route("/")
def home():
    """Startseite mit aktuellem Standardhintergrund"""
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    # Aktuellen Hintergrund merken
    if session.get("current_background") != background:
        session["current_background"] = background
        session.modified = True

    return render_template("home/home.html", background=background)


# =====================================
# EINSTELLUNGEN
# =====================================
@bp_main.route("/settings", methods=["GET", "POST"])
def settings():
    """Einstellungen für Standardbranch & Hintergründe"""
    defaults = {
        "default_branch": session.get("default_branch", "Heer"),
        "backgrounds": session.get("backgrounds", DEFAULT_BACKGROUNDS)
    }

    # Rücksprungziel
    next_page = request.args.get("next") or url_for("main.home")

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

        return redirect(request.form.get("next") or next_page)

    return render_template("settings/settings.html", defaults=defaults, next_page=next_page)


# =====================================
# DIENSTGRADE - MENÜ
# =====================================
@bp_ranks.route("/")
def ranks_menu():
    """Menü für den Bereich 'Dienstgrade'"""
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    # Hintergrund aktualisieren
    if session.get("current_background") != background:
        session["current_background"] = background
        session.modified = True

    return render_template("ranks/ranks_menu.html", background=background)


# =====================================
# DIENSTGRADE - TABELLE
# =====================================
@bp_ranks.route("/table")
def ranks_table():
    """Tabelle mit allen Dienstgraden (filterbar nach Truppenteil)"""
    branch = request.args.get("branch", session.get("default_branch", "Heer"))
    user_backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)

    if not branch or branch == "Alle":
        active_branch = session.get("default_branch", "Heer")
        background = user_backgrounds.get(active_branch, DEFAULT_BACKGROUNDS[active_branch])
        ranks = Rank.query.order_by(Rank.branch, Rank.sort_order).all()
    else:
        branch = branch.capitalize()
        background = user_backgrounds.get(branch, DEFAULT_BACKGROUNDS.get(branch))
        ranks = Rank.query.filter_by(branch=branch).order_by(Rank.sort_order).all()

    branches = ["Alle", "Heer", "Luftwaffe", "Marine"]
    session["current_background"] = background

    return render_template(
        "ranks/ranks_table.html",
        ranks=ranks,
        branches=branches,
        selected_branch=branch or "Alle",
        background=background
    )


# =====================================
# DIENSTGRADE - QUIZMODUS
# =====================================
@bp_ranks.route("/quizmodes")
def ranks_quizmodes():
    """Auswahl des Quizmodus für Dienstgrade"""
    branch = request.args.get("branch") or session.get("quiz_branch") or "Alle"
    mode = request.args.get("mode") or session.get("quiz_mode") or "normal"

    branches = ["Alle", "Heer", "Luftwaffe", "Marine"]
    session["quiz_branch"] = branch
    session["quiz_mode"] = mode
    session.modified = True

    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])
    session["current_background"] = background

    return render_template(
        "ranks/ranks_quizmodes.html",
        background=background,
        branches=branches,
        selected_branch=branch,
        selected_mode=mode
    )


# =====================================
# DIENSTGRADE - QUIZDATEN
# =====================================
def generate_quiz_data(branch=None):
    """Hilfsfunktion für Dienstgrad-Quizfragen"""
    branch = branch or session.get("quiz_branch", "Alle")

    if branch == "Alle":
        ranks = Rank.query.all()
    else:
        ranks = Rank.query.filter_by(branch=branch).all()

    if not ranks:
        ranks = Rank.query.all()

    correct = random.choice(ranks)
    wrong = random.sample([r for r in ranks if r.id != correct.id], min(3, len(ranks) - 1))

    options = [correct] + wrong
    random.shuffle(options)

    background = session.get("current_background", DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"]))

    return {"branch": branch, "background": background, "correct": correct, "options": options}


# =====================================
# DIENSTGRADE - QUIZSEITEN
# =====================================
@bp_ranks.route("/quiz1")
def ranks_quiz1():
    """Quiz: Text → Bild"""
    branch = request.args.get("branch")
    if branch:
        session["quiz_branch"] = branch
        session["current_background"] = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    data = generate_quiz_data()

    return render_template(
        "ranks/ranks_quiz1.html",
        correct=data["correct"],
        options=data["options"],
        background=data["background"],
        selected_branch=data["branch"]
    )


@bp_ranks.route("/quiz2")
def ranks_quiz2():
    """Quiz: Bild → Text"""
    branch = request.args.get("branch")
    if branch:
        session["quiz_branch"] = branch
        session["current_background"] = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    data = generate_quiz_data()

    return render_template(
        "ranks/ranks_quiz2.html",
        correct=data["correct"],
        options=data["options"],
        background=data["background"],
        selected_branch=data["branch"]
    )


# =====================================
# DIENSTGRADE - ZEITMODUS
# =====================================
@bp_ranks.route("/quiz1_timer")
def ranks_quiz1_timer():
    """Zeitmodus für Quiz 1"""
    branch = request.args.get("branch", session.get("quiz_branch", "Heer"))
    session["quiz_branch"] = branch

    ranks = Rank.query.filter_by(branch=branch).all() if branch != "Alle" else Rank.query.all()
    if not ranks:
        ranks = Rank.query.all()

    rank_data = [{
        "id": r.id,
        "title": r.title or "",
        "abbreviation": r.abbreviation or "",
        "rank_group": r.rank_group or "",
        "rank_type": r.rank_type or "",
        "level_code": r.level_code or "",
        "description": r.description or "",
        "image_filename": r.image_filename or "",
        "branch": r.branch or ""
    } for r in ranks]

    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])
    session["current_background"] = background

    return render_template("ranks/ranks_quiz1_timer.html", ranks=rank_data, background=background)


@bp_ranks.route("/quiz2_timer")
def ranks_quiz2_timer():
    """Zeitmodus für Quiz 2"""
    branch = request.args.get("branch", session.get("quiz_branch", "Heer"))
    session["quiz_branch"] = branch

    ranks = Rank.query.filter_by(branch=branch).all() if branch != "Alle" else Rank.query.all()
    if not ranks:
        ranks = Rank.query.all()

    rank_data = [{
        "id": r.id,
        "title": r.title or "",
        "abbreviation": r.abbreviation or "",
        "rank_group": r.rank_group or "",
        "rank_type": r.rank_type or "",
        "level_code": r.level_code or "",
        "description": r.description or "",
        "image_filename": r.image_filename or "",
        "branch": r.branch or ""
    } for r in ranks]

    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])
    session["current_background"] = background

    return render_template("ranks/ranks_quiz2_timer.html", ranks=rank_data, background=background)


# =====================================
# DIENSTGRADE - KARTEIKARTEN
# =====================================
@bp_ranks.route("/cards")
def ranks_cards():
    """Interaktive Karteikarten für Dienstgrade"""
    branch = request.args.get("branch", "Alle")
    query = Rank.query.filter_by(branch=branch) if branch != "Alle" else Rank.query
    ranks = query.order_by(Rank.branch, Rank.sort_order).all() or Rank.query.order_by(Rank.sort_order).all()

    rank_data = [{
        "id": r.id,
        "title": r.title,
        "abbreviation": r.abbreviation,
        "rank_group": r.rank_group,
        "rank_type": r.rank_type,
        "level_code": r.level_code,
        "description": r.description,
        "image_filename": r.image_filename,
        "branch": r.branch
    } for r in ranks]

    background = session.get("current_background", "Hintergrund-Heer-Wald.png")

    return render_template("ranks/ranks_cards.html", ranks=rank_data, background=background, selected_branch=branch)


# =====================================
# NATO-ALPHABET
# =====================================
@bp_nato.route("/")
def nato_menu():
    """Menüseite für den NATO-Alphabet-Bereich"""
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    if session.get("current_background") != background:
        session["current_background"] = background
        session.modified = True

    return render_template("nato/nato_menu.html", background=background)


# =====================================
# NATO-ALPHABET — TABELLE
# =====================================
@bp_nato.route("/table")
def nato_table():
    """Tabellarische Darstellung des NATO-Alphabets"""
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    nato_entries = NATO.query.order_by(NATO.letter.asc()).all()

    return render_template("nato/nato_table.html", entries=nato_entries, background=background)


# =====================================
# NATO-ALPHABET — KARTEIKARTEN
# =====================================
@bp_nato.route("/cards")
def nato_cards():
    """Karteikartenansicht des NATO-Alphabets"""
    # Hintergrund dynamisch nach Standard-Branch
    branch = session.get("default_branch", "Heer")
    backgrounds = session.get("backgrounds", DEFAULT_BACKGROUNDS)
    background = backgrounds.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    # Alle Buchstaben aus der DB laden (A–Z)
    nato_entries = NATO.query.order_by(NATO.letter.asc()).all()

    # JSON-kompatible Struktur für Template
    entries_data = [
        {
            "id": e.id,
            "letter": e.letter,
            "correct": e.correct,
            "wrongs": [
                e.wrong1, e.wrong2, e.wrong3, e.wrong4,
                e.wrong5, e.wrong6, e.wrong7, e.wrong8, e.wrong9
            ]
        }
        for e in nato_entries
    ]

    return render_template(
        "nato/nato_cards.html",
        entries=entries_data,
        background=background
    )


# =====================================
# NATO-ALPHABET — QUIZDATEN
# =====================================
def generate_nato_quiz_data():
    """Hilfsfunktion für NATO-Alphabet-Quizfragen (Daten aus DB)"""
    branch = session.get("default_branch", "Heer")
    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    entries = NATO.query.all()
    if not entries:
        return None

    # zufällige Zeile auswählen
    correct = random.choice(entries)

    # falsche Antworten aus derselben Zeile nehmen
    wrong_fields = [correct.wrong1, correct.wrong2, correct.wrong3,
                    correct.wrong4, correct.wrong5, correct.wrong6,
                    correct.wrong7, correct.wrong8, correct.wrong9]
    wrongs = [w for w in wrong_fields if w]

    # zufällig drei falsche auswählen
    wrong_selected = random.sample(wrongs, min(3, len(wrongs)))

    # Antwortoptionen zusammenstellen
    options = [correct.correct] + wrong_selected
    random.shuffle(options)

    return {
        "branch": branch,
        "background": background,
        "correct": correct.correct,
        "letter": correct.letter,
        "options": options
    }


# =====================================
# NATO-ALPHABET - QUIZSEITE
# =====================================
@bp_nato.route("/quizmodes")
def nato_quizmodes():
    """Menü zur Auswahl des Quizmodus (Unbegrenzt / Zeitmodus)"""
    mode = request.args.get("mode", "normal")
    session["nato_quiz_mode"] = mode

    branch = session.get("default_branch", "Heer")
    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    return render_template(
        "nato/nato_quizmodes.html",
        selected_mode=mode,
        background=background
    )


# =====================================
# NATO-ALPHABET - QUIZSEITE
# =====================================
@bp_nato.route("/quiz")
def nato_quiz():
    """Quiz: Welches Wort gehört zu diesem Buchstaben?"""
    data = generate_nato_quiz_data()
    if not data:
        return "Keine NATO-Daten in der Datenbank.", 500

    return render_template(
        "nato/nato_quiz.html",
        letter=data["letter"],
        correct=data["correct"],
        options=data["options"],
        background=data["background"]
    )


# =====================================
# NATO-ALPHABET - ZEITMODUS
# =====================================
@bp_nato.route("/quiz_timer")
def nato_quiz_timer():
    """Zeitmodus für NATO-Alphabet-Quiz"""
    nato_entries = NATO.query.all()
    if not nato_entries:
        return "Keine NATO-Daten gefunden.", 500

    branch = session.get("default_branch", "Heer")
    background = DEFAULT_BACKGROUNDS.get(branch, DEFAULT_BACKGROUNDS["Heer"])

    return render_template(
        "nato/nato_quiz_timer.html",
        nato_entries=nato_entries,
        background=background
    )