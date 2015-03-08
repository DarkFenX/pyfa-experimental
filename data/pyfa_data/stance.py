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


from data.eve_data.queries import get_type, get_attributes
from eos import Stance as EosStance


class Stance:

    def __init__(self, type_id):
        self.__type_id = type_id
        self.__ship = None
        self._eve_item = None
        self._eos_stance = EosStance(type_id)

    @property
    def eve_id(self):
        return self.__type_id

    @property
    def eve_name(self):
        return self._eve_item.name

    @property
    def attributes(self):
        eos_attrs = self._eos_stance.attributes
        attr_ids = eos_attrs.keys()
        attrs = get_attributes(self._ship._fit.source.edb, attr_ids)
        attr_map = {}
        for attr in attrs:
            attr_map[attr] = eos_attrs[attr.id]
        return attr_map

    @property
    def effects(self):
        return list(self._eve_item.effects)

    @property
    def _ship(self):
        return self.__ship

    @_ship.setter
    def _ship(self, new_ship):
        old_ship = self.__ship
        if new_ship is old_ship:
            return
        if old_ship is not None:
            old_fit = old_ship._fit
            if old_fit is not None:
                old_fit._stance_type_id = None
                old_fit._eos_fit.stance = None
        self.__ship = new_ship
        if new_ship is not None:
            new_fit = new_ship._fit
            if new_fit is not None:
                new_fit._stance_type_id = self.eve_id
                new_fit._eos_fit.stance = self._eos_stance
        self._update_source()

    def _update_source(self):
        try:
            source = self._ship._fit.source
        except AttributeError:
            self._eve_item = None
        else:
            self._eve_item = get_type(source.edb, self.eve_id)

    def __repr__(self):
        return '<Stance()>'
