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


from service.data.pyfa_data.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError
from service.data.pyfa_data.skill import SkillProxy

class RestrictedSet:
    """
    ABC for classes which provides same interface as regular
    set, but with getitem and delitem (using item type ID as
    key) on top of that. Several items with the same EVE ID
    cannot be added to such sets.
    """

    def __init__(self):
        self.__type_id_map = {}
        self.__set = set()

    def add(self, skill):
        type_id = skill.eve_id
        if type_id in self.__type_id_map:
            msg = 'skill with type ID {} already exists in this set'.format(type_id)
            raise ValueError(msg)
        self.__set.add(skill)
        self.__type_id_map[type_id] = skill

    def remove(self, skill):
        if skill not in self.__set:
            raise KeyError(skill)
        self.__set.remove(skill)
        del self.__type_id_map[skill.eve_id]

    def clear(self):
        for skill in list(self.__set):
            self.remove(skill)

    def __getitem__(self, eve_id):
        return self.__type_id_map[eve_id]

    def __delitem__(self, eve_id):
        skill = self[eve_id]
        self.remove(skill)

    def __iter__(self):
        return self.__set.__iter__()

    def __contains__(self, skill):
        return self.__set.__contains__(skill)

    def __len__(self):
        return self.__set.__len__()

    def __repr__(self):
        return repr(self.__set)


class SkillCoreSet(RestrictedSet):
    """
    This set is intended to be used on character cores.
    """

    def __init__(self, char_core):
        super().__init__()
        self.__char_core = char_core

    @property
    def _set(self):
        return self.__char_core._skills

    def add(self, skill):
        if skill._character is not None:
            raise ItemAlreadyUsedError(skill)
        super().add(skill)
        skill._character = self.__char_core
        for char_proxy in self.__char_core._proxy_iter():
            char_proxy.skills.add(SkillProxy(skill.eve_id, skill.level))

    def remove(self, skill):
        if skill._character is not self.__char_core:
            raise ItemRemovalConsistencyError(skill)
        super().remove(skill)
        for char_proxy in self.__char_core._proxy_iter():
            del char_proxy.skills[skill.eve_id]
        skill._character = None


class SkillProxySet(RestrictedSet):
    """
    This set is intended to be used on character proxies.
    """

    def __init__(self, char_proxy):
        super().__init__()
        self.__char_proxy = char_proxy

    def add(self, skill):
        if skill._char_proxy is not None:
            raise ItemAlreadyUsedError(skill)
        super().add(skill)
        skill._char_proxy = self.__char_proxy

    def remove(self, skill):
        if skill._char_proxy is not self.__char_proxy:
            raise ItemRemovalConsistencyError(skill)
        super().remove(skill)
        skill._char_proxy = None
