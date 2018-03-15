from __future__ import absolute_import

from flask import Flask

from burgers.models.meta import session
from burgers.models.burger import Burger

app = Flask(__name__)


@app.route("/burger", methods=["GET"])
def get_burgers():
    pass


@app.route("/burger", methods=["POST"])
def create_burger():
    pass


@app.route("/burger/<id>", methods=["PUT"])
def update_burger(id):
    pass


@app.route("/burger/<id>", methods=["DELETE"])
def delete_burger(id):
    pass

