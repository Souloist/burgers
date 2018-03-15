#!/usr/bin/env python

"""
Tool used to initialize burger tables.
"""

from __future__ import absolute_import

from burgers.models.meta import Base, engine
from burgers.models.burger import Burger


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
