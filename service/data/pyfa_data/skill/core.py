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


from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref, reconstructor

from eos import Skill as EosSkill
from service.data.pyfa_data.base import PyfaBase, EveItemWrapper
from util.repr import make_repr_str


class Skill(PyfaBase, EveItemWrapper):
    """
    This is "core" skill class (e.g. it will be used for managing
    character's skills in character editor). Fits will use proxy
    twin of this class to carry fit-specific attributes.

    Pyfa model: character_core.RestrictedSet(skills)
    Eos model: efit.RestrictedSet(skills)
    DB model: character_core.{_skills}
    """

    __tablename__ = 'skills'

    _db_character_id = Column('character_id', Integer, ForeignKey('characters.character_id'), primary_key=True)
    _db_character = relationship('Character', backref=backref(
        '_db_skills', collection_class=set, cascade='all, delete-orphan'))

    _db_type_id = Column('type_id', Integer, nullable=False)
    _db_level = Column(Integer, nullable=False)

    def __init__(self, type_id, level=0):
        self._db_type_id = type_id
        self._db_level = level
        self.__generic_init()

    @reconstructor
    def _dbinit(self):
        self.__generic_init()

    def __generic_init(self):
        EveItemWrapper.__init__(self, self._db_type_id)
        self.__parent_char_core = None
        self.__eos_skill = EosSkill(self._db_type_id, level=self._db_level)

    # EVE item wrapper methods
    @property
    def _source(self):
        try:
            return self._parent_char_core.source
        except AttributeError:
            return None

    @property
    def _eos_item(self):
        return self.__eos_skill

    # Skill-specific methods
    @property
    def level(self):
        return self._db_level

    @level.setter
    def level(self, new_level):
        old_level = self.level
        if new_level == old_level:
            return
        # Update DB
        self._db_level = new_level
        # Update proxies of this skill
        for char_proxy in self._parent_char_core._proxy_iter():
            char_proxy.skills[self.eve_id]._set_level(new_level)

    # Auxiliary methods
    @property
    def _parent_char_core(self):
        return self.__parent_char_core

    @_parent_char_core.setter
    def _parent_char_core(self, new_char_core):
        old_char_core = self._parent_char_core
        # Update DB and Eos
        self._unregister_on_char_core(old_char_core)
        # Update parent reference
        self.__parent_char_core = new_char_core
        # Update DB and Eos
        self._register_on_char_core(new_char_core)
        # Update EVE item
        self._update_source()

    def _register_on_char_core(self, char_core):
        if char_core is not None:
            # Update DB
            char_core._db_skills.add(self)
            # Update Eos
            char_core._eos_fit.skills.add(self.__eos_skill)

    def _unregister_on_char_core(self, char_core):
        if char_core is not None:
            # Update DB
            char_core._db_skills.remove(self)
            # Update Eos
            char_core._eos_fit.skills.remove(self.__eos_skill)

    def __repr__(self):
        spec = ['eve_id', 'level']
        return make_repr_str(self, spec)
