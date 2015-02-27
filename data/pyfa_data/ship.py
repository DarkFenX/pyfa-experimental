#===============================================================================
# Copyright (C) 2015 Anton Vorobyov
#
# This file is part of Pyfa 3.
#
# Pyfa 3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyfa 3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyfa 3. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from sqlalchemy import Column, Integer

from data.eve_data.queries import get_type, get_attributes
from eos import Ship as EosShip
from .base import PyfaBase


class Ship(PyfaBase):

    __tablename__ = 'ships'

    _id = Column('ship_id', Integer, primary_key=True)
    _type_id = Column('type_id', Integer, nullable=False)

    def __init__(self, type_id):
        self._type_id = type_id
        self.__fit = None
        self._eve_item = None
        self._eos_ship = EosShip(type_id)

    @property
    def eve_id(self):
        return self._type_id

    @property
    def eve_name(self):
        return self._eve_item.name

    @property
    def attributes(self):
        eos_attrs = self._eos_ship.attributes
        attr_ids = eos_attrs.keys()
        attrs = get_attributes(self._fit.source.edb, attr_ids)
        attr_map = {}
        for attr in attrs:
            attr_map[attr] = eos_attrs[attr.id]
        return attr_map

    @property
    def effects(self):
        return list(self._eve_item.effects)

    @property
    def _fit(self):
        return self.__fit

    @_fit.setter
    def _fit(self, new_fit):
        self.__fit = new_fit
        self._update_source()

    def _update_source(self):
        self._eve_item = get_type(self._fit.source.edb, self.eve_id)
