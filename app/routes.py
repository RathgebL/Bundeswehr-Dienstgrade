from flask import Blueprint, render_template
from .models import Rank

bp = Blueprint('main', __name__)

@bp.route("/")
def home():
    ranks = Rank.query.all()
    return render_template("ranks.html", ranks=ranks)