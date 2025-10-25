from flask import Blueprint, render_template, request
from .models import Rank

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    # Optional: Dropdown-Filter (z. B. ?branch=Heer)
    branch = request.args.get("branch")
    query = Rank.query
    if branch:
        query = query.filter_by(branch=branch)

    ranks = query.order_by(Rank.branch, Rank.sort_order).all()
    branches = ["Heer", "Luftwaffe", "Marine"]

    return render_template("ranks.html", ranks=ranks, branches=branches, selected_branch=branch)