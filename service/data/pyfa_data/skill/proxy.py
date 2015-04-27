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


from eos import Skill as EosSkill
from service.data.pyfa_data.base import EveItemWrapper
from util.repr import make_repr_str


class SkillProxy(EveItemWrapper):
    """
    Pyfa model: character_proxy.{skills}
    Eos model: efit.{skills}
    DB model: none (SkillCore handles it)
    """

    def __init__(self, type_id, level):
        EveItemWrapper.__init__(self, type_id)
        self.__char_proxy = None
        self.__eos_skill = EosSkill(type_id, level=level)

    # Pyfa fit item methods
    @property
    def _source(self):
        try:
            return self._char_proxy._fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_skill

    # Skill-specific methods
    @property
    def level(self):
        return self.__eos_skill.level

    def _set_level(self, new_level):
        self.__eos_skill.level = new_level

    # Auxiliary methods
    @property
    def _char_proxy(self):
        return self.__char_proxy

    @_char_proxy.setter
    def _char_proxy(self, new_char_proxy):
        old_char_proxy = self._char_proxy
        old_fit = getattr(old_char_proxy, '_fit', None)
        new_fit = getattr(new_char_proxy, '_fit', None)
        # Update DB and Eos
        self._unregister_on_fit(old_fit)
        # Update reverse reference
        self.__char_proxy = new_char_proxy
        # Update DB and Eos
        self._register_on_fit(new_fit)
        # Update EVE item
        self._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # DB update is not needed
            # Update Eos
            fit._eos_fit.skills.add(self.__eos_skill)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # DB update is not needed
            # Update Eos
            fit._eos_fit.skills.remove(self.__eos_skill)

    def __repr__(self):
        spec = ['eve_id', 'level']
        return make_repr_str(self, spec)
