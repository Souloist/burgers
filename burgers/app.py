from __future__ import absolute_import

from flask import Flask, jsonify, request, abort
from cerberus import Validator

from burgers.models.meta import session
from burgers.models.burger import Burger

app = Flask(__name__)


@app.route("/burger", methods=["GET"])
def get_burgers():
    """Returns all burgers for a given topping."""

    valid_toppings = (
        "has_cheese",
        "has_bun",
        "has_patty",
        "has_lettuce",
        "has_ketchup",
    )

    topping = request.args.get("topping")
    if topping is None:
        burgers = session.query(Burger).all()
        burger_list = {_get_burger_attributes(burger) for burger in burgers}

        return burger_list

    if topping not in valid_toppings:
        return abort(422, {"error": "Please supply a valid topping"})


def _get_burger_attributes(burger):
    """Returns attributes of a models.Burger instance as a dictionary.

    :param burger: Instance of models.Burger

    """

    return {
        "id": burger.id,
        "has_cheese": burger.has_cheese,
        "has_bun": burger.has_bun,
        "has_patty": burger.has_patty,
        "has_lettuce": burger.has_lettuce,
        "has_ketchup": burger.has_ketchup,
    }


@app.route("/burger", methods=["POST"])
def create_burger():
    """Creates a burger from the incoming request. Will return with an
    error if the request is formatted incorrectly or missing body.
    """

    burger_schema = Validator({
        "has_cheese": {"type": "string"},
        "has_bun": {"type": "string"},
        "has_patty": {"type": "string"},
        "has_lettuce": {"type": "string"},
        "has_ketchup": {"type": "string"},
    })

    json = request.json

    if not json:
        return abort(400)

    if burger_schema.validate(json):
        return abort(422, {"error": "Missing parameters"})

    new_burger = Burger(
        has_cheese=json["has_cheese"],
        has_bun=json["has_bun"],
        has_patty=json["has_patty"],
        has_lettuce=json["has_lettuce"],
        has_ketchup=json["has_ketchup"],
    )

    session.add(new_burger)
    session.commit()

    return jsonify(new_burger)


@app.route("/burger/<int:id>", methods=["PUT"])
def update_burger(id):
    """Updates the burger's toppings based on the incoming request.
    If the burger cannot be found, an error is returned.
    """

    burger = session.query(Burger).get(id)

    if burger is None:
        return abort(400)

    burger.has_cheese = request.json.get("has_cheese", burger.has_cheese)
    burger.has_bun = request.json.get("has_bun", burger.has_bun)
    burger.has_patty = request.json.get("has_patty", burger.has_patty)
    burger.has_lettuce = request.json.get("has_lettuce", burger.has_lettuce)
    session.commit()

    return jsonify(burger)


@app.route("/burger/<int:id>", methods=["DELETE"])
def delete_burger(id):
    """Deletes a burger based off id. If the burger cannot be found, it will
    return an error message.
    """

    burger = session.query(Burger).get(id)

    if burger is None:
        return abort(422, {"error": "Burger does not exist"})

    session.delete(burger)
    session.commit()

    return jsonify({"Success": True})
