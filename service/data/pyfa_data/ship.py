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

from eos import Ship as EosShip
from service.data.eve_data.queries import get_type, get_attributes
from service.util.repr import make_repr_str
from .aux.command import BaseCommand
from .aux.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError
from .aux.src_children import get_src_children


class Ship:
    """
    Pyfa model: fit.ship
    Eos model: fit.ship
    DB model: fit._ship_type_id

    Pyfa model children:
      stance
    """

    def __init__(self, type_id, stance=None):
        self.__type_id = type_id
        self.__fit = None
        self.__stance = None
        self._eve_item = None
        self._eos_ship = EosShip(type_id)
        self.stance = stance

    # Read-only info
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

    # Children getters/setters
    @property
    def stance(self):
        return self.__stance

    @stance.setter
    def stance(self, new_stance):
        command = ShipStanceChangeCommand(self, new_stance)
        try:
            cmd_mgr = self._fit._cmd_mgr
        except AttributeError:
            command.run()
        else:
            cmd_mgr.do(command)

    def _set_stance(self, new_stance):
        old_stance = self.__stance
        if new_stance is old_stance:
            return
        if old_stance is not None:
            if old_stance._ship is None:
                raise ItemRemovalConsistencyError(old_stance)
            old_stance._ship = None
        self.__stance = new_stance
        if new_stance is not None:
            if new_stance._ship is not None:
                raise ItemAlreadyUsedError(new_stance)
            new_stance._ship = self

    # Auxiliary methods
    @property
    def _fit(self):
        return self.__fit

    @_fit.setter
    def _fit(self, new_fit):
        old_fit = self._fit
        self._unregister_on_fit(old_fit)
        self.__fit = new_fit
        self._register_on_fit(new_fit)
        self._update_source()
        for src_child in self._src_children:
            src_child._update_source()

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
    def _src_children(self):
        return get_src_children(chain(
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
        spec = ['eve_id']
        return make_repr_str(self, spec)


class ShipStanceChangeCommand(BaseCommand):

    def __init__(self, ship, new_stance):
        self.__executed = False
        self.ship = ship
        self.old_stance = ship.stance
        self.new_stance = new_stance

    def run(self):
        self.ship._set_stance(self.new_stance)
        self.__executed = True

    def reverse(self):
        self.ship._set_stance(self.old_stance)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())
