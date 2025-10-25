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
    # Aktuelle oder Standardwerte laden
    defaults = {
        "default_branch": session.get("default_branch", "Heer"),
        "backgrounds": session.get("backgrounds", DEFAULT_BACKGROUNDS)
    }

    if request.method == "POST":
        # Ausgewählten Standard-Truppenteil speichern
        branch_input = request.form.get("default_branch", "Heer").strip().capitalize()
        session["default_branch"] = branch_input

        # Benutzerdefinierte Hintergründe speichern (alle 3 Truppenteile)
        backgrounds = {
            "Heer": request.form.get("bg_heer", defaults["backgrounds"].get("Heer")),
            "Luftwaffe": request.form.get("bg_luftwaffe", defaults["backgrounds"].get("Luftwaffe")),
            "Marine": request.form.get("bg_marine", defaults["backgrounds"].get("Marine"))
        }

        # Sicherheit: Alle Keys groß schreiben
        backgrounds = {key.capitalize(): value for key, value in backgrounds.items()}

        # Session aktualisieren
        session["backgrounds"] = backgrounds
        session.modified = True

        # Debug-Ausgabe (zum Testen, später entfernen)
        print("SESSION BACKGROUNDS:", session["backgrounds"])
        print("DEFAULT BRANCH:", session["default_branch"])

        return redirect(url_for("main.index"))

    # Seite anzeigen
    return render_template("settings.html", defaults=defaults)

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

# Quiz
@bp.route("/quiz")
def quiz():
    # Alle Dienstgrade laden
    ranks = Rank.query.all()

    # Einen richtigen und drei falsche auswählen
    correct = random.choice(ranks)
    wrong = random.sample([r for r in ranks if r.id != correct.id], 3)

    options = [correct] + wrong
    random.shuffle(options)

    # Aktuellen Hintergrund übernehmen (aus Session)
    background = session.get("current_background", DEFAULT_BACKGROUNDS["Heer"])

    return render_template("quiz.html", correct=correct, options=options, background=background)

# Karteikarten
@bp.route("/flashcards")
def flashcards():
    ranks = Rank.query.order_by(Rank.branch, Rank.sort_order).all()

    # Konvertiere zu JSON-kompatiblen Dictionaries
    rank_data = [
        {
            "id": r.id,
            "title": r.title,
            "abbreviation": r.abbreviation,
            "rank_group": r.rank_group,
            "rank_type": r.rank_type,
            "level_code": r.level_code,
            "description": r.description,
            "image_filename": r.image_filename
        }
        for r in ranks
    ]

    background = session.get("current_background", "Hintergrund-Heer-Wald.png")

    return render_template("flashcards.html", ranks=rank_data, background=background)