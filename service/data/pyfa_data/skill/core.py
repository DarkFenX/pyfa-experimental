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

from service.data.pyfa_data.base import PyfaBase
from util.repr import make_repr_str


class Skill(PyfaBase):
    """
    This is "core" skill class (e.g. it will be used for managing
    character's skills in character editor). Fits will use proxy
    twin of this class to carry fit-specific attributes.

    Pyfa model: character_core.RestrictedSet(skills)
    Eos model: efit.RestrictedSet(skills)
    DB model: character_core.{_skills}
    """

    __tablename__ = 'skills'

    _character_id = Column('character_id', Integer, ForeignKey('characters.character_id'), primary_key=True)
    eve_id = Column('type_id', Integer, primary_key=True)
    _level = Column(Integer, nullable=False)

    def __init__(self, type_id, level=0):
        self.eve_id = type_id
        self._level = level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        old_level = self.level
        if new_level == old_level:
            return
        # Update DB
        self._level = new_level
        # Update proxies of this skill
        for char_proxy in self._character._proxy_iter():
            char_proxy.skills[self.eve_id]._set_level(new_level)

    # Auxiliary methods
    def __repr__(self):
        spec = ['eve_id', 'level']
        return make_repr_str(self, spec)
