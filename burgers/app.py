from __future__ import absolute_import

from flask import Flask, jsonify, request, abort
from cerberus import Validator
from distutils.util import strtobool

from burgers.models.meta import session
from burgers.models.burger import Burger

app = Flask(__name__)


@app.route("/burger", methods=["GET"])
def get_burgers():
    """Returns all burgers for a given topping. Will return all burgers
    if no topping is provided."""

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
        formatted_burgers = _format_burgers_into_dict(burgers)
        return jsonify(formatted_burgers)

    if topping not in valid_toppings:
        return abort(422, {"error": "Please supply a valid topping"})

    burgers_with_topping = session.execute(
        "SELECT * FROM burgers where {} = True;".format(topping)
    )

    formatted_burgers_with_topping = _format_burgers_into_dict(burgers_with_topping)
    return jsonify(formatted_burgers_with_topping)


def _format_burgers_into_dict(burgers):
    """Returns a formatted dictionary give an iterable of models.Burger instances.

    :param burgers: Interable containing models.Burger instances

    """
    return {burger.id: _get_burger_attributes(burger) for burger in burgers}


def _get_burger_attributes(burger):
    """Returns attributes of a models.Burger instance as a dictionary.

    :param burger: Instance of models.Burger

    """

    return {
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

    json = request.json

    burger_schema = Validator({
        "has_cheese": {"type": "boolean"},
        "has_bun": {"type": "boolean"},
        "has_patty": {"type": "boolean"},
        "has_lettuce": {"type": "boolean"},
        "has_ketchup": {"type": "boolean"},
    })

    if not json:
        return abort(400)

    if burger_schema.validate(json):
        return abort(422, {"error": "Missing parameters"})

    new_burger = Burger(
        has_cheese=strtobool(json["has_cheese"]),
        has_bun=strtobool(json["has_bun"]),
        has_patty=strtobool(json["has_patty"]),
        has_lettuce=strtobool(json["has_lettuce"]),
        has_ketchup=strtobool(json["has_ketchup"]),
    )

    session.add(new_burger)
    session.commit()

    return jsonify({"burger": _get_burger_attributes(new_burger)}), 201


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

    return jsonify({"burger": _get_burger_attributes(burger)}), 200


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
