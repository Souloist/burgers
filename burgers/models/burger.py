from __future__ import absolute_import

from sqlalchemy import Column, Integer, Boolean
from burgers.models.meta import Base


class Burger(Base):
    __tablename__ = "burgers"

    id = Column(Integer, primary_key=True)
    has_cheese = Column(Boolean, default=False, server_default="false")
    has_bun = Column(Boolean, default=False, server_default="false")
    has_patty = Column(Boolean, default=False, server_default="false")
    has_lettuce = Column(Boolean, default=False, server_default="false")
    has_ketchup = Column(Boolean, default=False, server_default="false")

