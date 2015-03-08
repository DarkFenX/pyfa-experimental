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


from itertools import chain

from data.eve_data.queries import get_type, get_attributes
from eos import Ship as EosShip
from .aux import get_children


class Ship:

    def __init__(self, type_id, stance=None):
        self.__type_id = type_id
        self.__fit = None
        self.__stance = None
        self._eve_item = None
        self._eos_ship = EosShip(type_id)
        self.stance = stance

    @property
    def stance(self):
        return self.__stance

    @stance.setter
    def stance(self, new_stance):
        old_stance = self.__stance
        if old_stance is not None:
            old_stance._ship = None
        self.__stance = new_stance
        if new_stance is not None:
            new_stance._ship = self

    @property
    def eve_id(self):
        return self.__type_id

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
        """
        Handle fit switch for ship and all its child objects.
        """
        old_fit = self._fit
        if new_fit is old_fit:
            return
        self._unregister_on_fit(old_fit)
        self.__fit = new_fit
        self._register_on_fit(new_fit)
        self._update_source()

    def  _register_on_fit(self, fit):
        if fit is not None:
            fit._ship_type_id = self.eve_id
            fit._eos_fit.ship = self._eos_ship
            if self.stance is not None:
                self.stance._register_on_fit(fit)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            fit._ship_type_id = None
            fit._eos_fit.ship = None
            if self.stance is not None:
                self.stance._unregister_on_fit(fit)

    @property
    def _children(self):
        return get_children(chain(
            (self.stance,)
        ))

    def _update_source(self):
        try:
            source = self._fit.source
        except AttributeError:
            self._eve_item = None
        else:
            self._eve_item = get_type(source.edb, self.eve_id)

    def __repr__(self):
        return '<Ship(eve_id={})>'.format(self.eve_id)
