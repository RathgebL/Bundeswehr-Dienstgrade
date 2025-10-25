from flask import Blueprint, render_template, request
from .models import Rank
import random

bp = Blueprint("main", __name__)

# Startseite
@bp.route("/")
def index():
    return render_template("index.html")

# Tabelle
@bp.route("/ranks")
def ranks():
    # Optional: Dropdown-Filter (z. B. ?branch=Heer)
    branch = request.args.get("branch")
    query = Rank.query
    if branch:
        query = query.filter_by(branch=branch)

    ranks = query.order_by(Rank.branch, Rank.sort_order).all()
    branches = ["Heer", "Luftwaffe", "Marine"]

    return render_template("ranks.html", ranks=ranks, branches=branches, selected_branch=branch)

# Quiz
@bp.route("/quiz")
def quiz():
    # alle Dienstgrade laden
    ranks = Rank.query.all()

    # 1 richtigen zufällig wählen
    correct = random.choice(ranks)

    # 3 falsche Antworten (ohne den richtigen)
    wrong = random.sample([r for r in ranks if r.id != correct.id], 3)

    # Antworten mischen
    options = [correct] + wrong
    random.shuffle(options)

    return render_template("quiz.html", correct=correct, options=options)