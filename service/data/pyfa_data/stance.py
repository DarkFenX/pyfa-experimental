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


from eos import Stance as EosStance
from service.data.eve_data.query import get_type, get_attributes
from service.util.repr import make_repr_str


class Stance:
    """
    Pyfa model: ship.stance
    Eos model: efit.stance
    DB model: fit._stance_type_id
    """

    def __init__(self, type_id):
        self._type_id = type_id
        self.__ship = None
        self._eve_item = None
        self._eos_stance = EosStance(type_id)

    # Read-only info
    @property
    def eve_id(self):
        return self._type_id

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

    # Auxiliary methods
    @property
    def _ship(self):
        return self.__ship

    @_ship.setter
    def _ship(self, new_ship):
        old_ship = self._ship
        old_fit = getattr(old_ship, '_fit', None)
        new_fit = getattr(new_ship, '_fit', None)
        # Update DB and Eos
        self._unregister_on_fit(old_fit)
        # Update reverse reference
        self.__ship = new_ship
        # Update DB and Eos
        self._register_on_fit(new_fit)
        # Update EVE item
        self._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._stance_type_id = self.eve_id
            # Update Eos
            fit._eos_fit.stance = self._eos_stance

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._stance_type_id = None
            # Update Eos
            fit._eos_fit.stance = None

    def _update_source(self):
        try:
            source = self._ship._fit.source
        except AttributeError:
            self._eve_item = None
        else:
            if source is not None:
                self._eve_item = get_type(source.edb, self.eve_id)
            else:
                self._eve_item = None

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
