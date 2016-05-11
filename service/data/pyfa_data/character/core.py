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
from weakref import WeakSet

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import reconstructor

from eos import Fit as EosFit
from service.data.pyfa_data.base import PyfaBase, EveItemWrapper
from service.data.pyfa_data.func import get_src_children, pyfa_persist, pyfa_abandon
from service.source import SourceManager, Source
from util.const import Type
from util.repr import make_repr_str
from .container import SkillCoreSet


class Character(PyfaBase, EveItemWrapper):
    """
    "Core" character class. It should be used for managing characters
    (e.g. in character editor). Fits will use proxy twin of the character.
    We cannot use core because different fits carry different attributes
    on character and all child entities (like skills, on-character
    implants, and so on).

    Pyfa model children:
    .RestrictedSet(skills)
    """

    __tablename__ = 'characters'

    id = Column('character_id', Integer, primary_key=True)
    alias = Column(String)

    def __init__(self, alias='', source=None):
        self.alias = alias
        self.__generic_init()
        # Use default source, unless specified otherwise
        if source is None:
            source = SourceManager.default
        self.source = source

    @reconstructor
    def _dbinit(self):
        self.__generic_init()
        # Use default source for all reconstructed characters
        self.source = SourceManager.default
        # Restore entities which are stored on character
        for skill in self._db_skills:
            self.skills.add(skill)

    def __generic_init(self):
        char_type_id = Type.character_static
        EveItemWrapper.__init__(self, char_type_id)
        # Attributes which store objects hidden behind properties
        self.__source = None
        # Set with fits which are loaded and use this character
        self.__loaded_proxies = WeakSet()
        self.skills = SkillCoreSet(self)
        self._eos_fit = EosFit()

    # EVE item wrapper methods
    @property
    def _source(self):
        return self.source

    @property
    def _eos_item(self):
        return self._eos_fit.character

    @property
    def _src_children(self):
        return get_src_children(chain(
            self.skills,
        ))

    # Miscellanea public stuff
    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        # Attempt to fetch source from source manager if passed object
        # is not instance of source class
        if not isinstance(new_source, Source) and new_source is not None:
            new_source = SourceManager.get(new_source)
        old_source = self.source
        # Do not update anything if sources are the same
        if new_source is old_source:
            return
        self.__source = new_source
        # Update eos model with new data
        self._eos_fit.source = getattr(new_source, 'eos', None)
        # Update pyfa model with new data
        # Unlike fit, character represents EVE item, thus we need
        # to update it too
        self._update_source()
        for src_child in self._src_children:
            src_child._update_source()

    persist = pyfa_persist
    abandon = pyfa_abandon

    def validate(self):
        self._eos_fit.validate()

    # Auxiliary methods
    def _proxy_iter(self):
        """
        Safe iterator over related character proxies, avoids issues
        with set size getting changed by GC during iteration.
        """
        for char_proxy in tuple(self.__loaded_proxies):
            yield char_proxy

    def _link_proxy(self, char_proxy):
        """Create connection between character core and proxy"""
        self.__loaded_proxies.add(char_proxy)

    def _unlink_proxy(self, char_proxy):
        """Remove connection between character core and proxy"""
        self.__loaded_proxies.discard(char_proxy)

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
