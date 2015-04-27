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


from weakref import WeakSet

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, reconstructor

from service.data.pyfa_data.base import PyfaBase
from service.data.pyfa_data.func import pyfa_persist, pyfa_abandon
from util.repr import make_repr_str
from .container import CoreSkillSet


class Character(PyfaBase):
    """
    "Core" character class. It will be used for managing characters (e.g.
    in character editor). Fits will use proxy twin of the character. We
    cannot use core because different fits carry different attributes on
    character and all child entities (like skills, on-character implants,
    and so on).

    Pyfa model children:
    .{skills}
    """

    __tablename__ = 'characters'

    id = Column('character_id', Integer, primary_key=True)
    alias = Column(String)

    _skills = relationship('Skill', collection_class=set, cascade='all, delete-orphan', backref='_character')

    def __init__(self, alias=''):
        self.alias = alias
        self.__generic_init()

    @reconstructor
    def _dbinit(self):
        self.__generic_init()

    def __generic_init(self):
        self.skills = CoreSkillSet(self)
        # Set with fits which are loaded and use this character
        self._loaded_proxies = WeakSet()

    # Miscellanea public stuff
    persist = pyfa_persist
    abandon = pyfa_abandon

    # Auxiliary methods
    def _proxy_iter(self):
        """
        Safe iterator over related character proxies, avoids issues
        with set size getting changed by GC during iteration.
        """
        for char_proxy in tuple(self._loaded_proxies):
            yield char_proxy

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
