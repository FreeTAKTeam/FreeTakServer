from flask import Blueprint

page = Blueprint('citrap', __name__)

@page.route("/Marti/api/citrap")
def get_citraps():
    return "[]"