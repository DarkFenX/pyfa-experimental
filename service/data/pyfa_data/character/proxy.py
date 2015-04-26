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


from eos import Character as EosCharacter
from service.data.pyfa_data.base import FitItemBase
from service.data.pyfa_data.func import get_src_children
from util.const import Type
from util.repr import make_repr_str


class CharacterProxy(FitItemBase):

    def __init__(self):
        char_typeid = Type.character_static
        FitItemBase.__init__(self, char_typeid)
        self.__fit = None
        self.__eos_char = EosCharacter(char_typeid)

    # Pyfa fit item methods
    @property
    def _source(self):
        try:
            return self._fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_char

    @property
    def _src_children(self):
        return ()

    # Character-specific readonly data
    @property
    def alias(self):
        try:
            return self.__core.alias
        except AttributeError:
            return None

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
            # Update Eos
            fit._eos_fit.character = self.__eos_char
            # Update DB and Eos for children

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # Update Eos
            fit._eos_fit.character = None
            # Update DB and Eos for children

    @property
    def __core(self):
        """
        Reference to character core.
        """
        try:
            return self._fit.character_core
        except AttributeError:
            return None

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
