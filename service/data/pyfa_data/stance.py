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
from service.data.pyfa_data.base import EveItemWrapper
from util.repr import make_repr_str


class Stance(EveItemWrapper):
    """
    Pyfa model: ship.stance
    Eos model: efit.stance
    DB model: fit._db_stance_type_id
    """

    def __init__(self, type_id):
        EveItemWrapper.__init__(self, type_id)
        self.__parent_ship = None
        self.__eos_stance = EosStance(type_id)

    # EVE item wrapper methods
    @property
    def _source(self):
        try:
            return self._parent_ship._parent_fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_stance

    # Auxiliary methods
    @property
    def _parent_ship(self):
        return self.__parent_ship

    @_parent_ship.setter
    def _parent_ship(self, new_ship):
        old_ship = self._parent_ship
        old_fit = getattr(old_ship, '_parent_fit', None)
        new_fit = getattr(new_ship, '_parent_fit', None)
        # Update DB and Eos
        self._unregister_on_fit(old_fit)
        # Update parent reference
        self.__parent_ship = new_ship
        # Update DB and Eos
        self._register_on_fit(new_fit)
        # Update EVE item
        self._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._db_stance_type_id = self.eve_id
            # Update Eos
            fit._eos_fit.stance = self.__eos_stance

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._db_stance_type_id = None
            # Update Eos
            fit._eos_fit.stance = None

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
