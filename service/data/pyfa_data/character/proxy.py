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

from eos import Character as EosCharacter
from service.data.pyfa_data.base import EveItemWrapper
from service.data.pyfa_data.func import get_src_children
from service.data.pyfa_data.skill import SkillProxy
from util.const import Type
from util.repr import make_repr_str
from .container import SkillProxySet


class CharacterProxy(EveItemWrapper):
    """
    "Proxy" character class. It's directly attached to fit and carries
    fit-specific attributes. Exposes regular fit item interface (with
    attributes, effects and so on). On top of that, exposes some
    of core character data.

    Pyfa model: fit.character_proxy
    Eos model: efit.character
    DB model: none (CharacterCore handles it)

    Pyfa model children:
    .RestrictedSet(skills)
    """

    def __init__(self):
        char_type_id = Type.character_static
        EveItemWrapper.__init__(self, char_type_id)
        self.__parent_fit = None
        self.__parent_char_core = None
        self.skills = SkillProxySet(self)
        self.__eos_char = EosCharacter(char_type_id)

    # EVE item wrapper methods
    @property
    def _source(self):
        try:
            return self._parent_fit.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_char

    @property
    def _src_children(self):
        return get_src_children(chain(
            self.skills,
        ))

    # Character core data shortcuts
    @property
    def alias(self):
        try:
            return self._parent_char_core.alias
        except AttributeError:
            return None

    # Auxiliary methods
    @property
    def _parent_fit(self):
        return self.__parent_fit

    @_parent_fit.setter
    def _parent_fit(self, new_fit):
        old_fit = self._parent_fit
        # Update DB and Eos for self and children
        self._unregister_on_fit(old_fit)
        # Update parent reference
        self.__parent_fit = new_fit
        # Update DB and Eos for self and children
        self._register_on_fit(new_fit)
        # Update EVE item for self and children
        self._update_source()
        for src_child in self._src_children:
            src_child._update_source()

    def _register_on_fit(self, fit):
        if fit is not None:
            # DB update for self & children is not needed for proxies
            # Update Eos
            fit._eos_fit.character = self.__eos_char
            # Update Eos for children
            for skill in self.skills:
                skill._register_on_fit(fit)

    def _unregister_on_fit(self, fit):
        if fit is not None:
            # DB update for self & children is not needed for proxies
            # Update Eos
            fit._eos_fit.character = None
            # Update Eos for children
            for skill in self.skills:
                skill._unregister_on_fit(fit)

    @property
    def _parent_char_core(self):
        return self.__parent_char_core

    @_parent_char_core.setter
    def _parent_char_core(self, new_char_core):
        old_char_core = self._parent_char_core
        # Handle proxy reference on old character core
        if old_char_core is not None:
            old_char_core._unlink_proxy(self)
        # Update parent reference
        self.__parent_char_core = new_char_core
        # Run updates on various child objects using data from
        # new character core
        self.__update_skills(new_char_core)
        # Handle proxy reference on new character core
        if new_char_core is not None:
            new_char_core._link_proxy(self)

    def __update_skills(self, new_char_core):
        # Gather data about skill levels
        current_skills = self.skills
        new_skills = getattr(new_char_core, 'skills', ())
        # {type ID: level}
        current_levels = {}
        new_levels = {}
        for skill in current_skills:
            current_levels[skill.eve_id] = skill.level
        for skill in new_skills:
            new_levels[skill.eve_id] = skill.level
        # Find out what we actually need to do
        to_remove = set(current_levels).difference(new_levels)
        to_change = set(filter(
            lambda tid: current_levels[tid] != new_levels[tid],
            set(current_levels).intersection(new_levels)
        ))
        to_add = set(new_levels).difference(current_levels)
        # And finally, do planned updates
        for type_id in to_remove:
            del current_skills[type_id]
        for type_id in to_change:
            current_skills[type_id]._set_level(new_levels[type_id])
        for type_id in to_add:
            current_skills.add(SkillProxy(type_id, new_levels[type_id]))

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
