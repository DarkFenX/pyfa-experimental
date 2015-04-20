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
from service.data.pyfa_data.base import FitItemBase
from service.data.pyfa_data.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError
from service.data.pyfa_data.func import get_src_children
from util.repr import make_repr_str
from .command import *
from .container import *


class Ship(FitItemBase):
    """
    Pyfa model: fit.ship
    Eos model: efit.ship
    DB model: fit._ship_type_id

    Pyfa model children:
      .stance
      .{subsystems}
    """

    def __init__(self, type_id, stance=None):
        FitItemBase.__init__(self, type_id)
        self.__fit = None
        self.__stance = None
        self._eve_item = None
        self._eos_ship = EosShip(type_id)
        self.subsystems = SubsystemSet(self)
        self.stance = stance

    # Implementation of abstract methods for pyfa fit item
    @property
    def _source(self):
        try:
            return self._fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self._eos_ship

    @property
    def _src_children(self):
        return get_src_children(chain(
            (self.stance,),
            self.subsystems
        ))

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
        # Update forward reference
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
        # Update DB and Eos for self and children
        self._unregister_on_fit(old_fit)
        # Update reverse reference
        self.__fit = new_fit
        # Update DB and Eos for self and children
        self._register_on_fit(new_fit)
        # Update EVE item for self and children
        self._update_source()
        for src_child in self._src_children:
            src_child._update_source()

    def  _register_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._ship_type_id = self.eve_id
            # Update Eos
            fit._eos_fit.ship = self._eos_ship
            # Update DB and Eos for children
            if self.stance is not None:
                self.stance._register_on_fit(fit)
            for subsystem in self.subsystems:
                subsystem._register_on_fit(fit)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update DB
            fit._ship_type_id = None
            # Update Eos
            fit._eos_fit.ship = None
            # Update DB and Eos for children
            if self.stance is not None:
                self.stance._unregister_on_fit(fit)
            for subsystem in self.subsystems:
                subsystem._unregister_on_fit(fit)

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
