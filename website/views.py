from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
# @login_required
def home():
    return render_template("index.html")