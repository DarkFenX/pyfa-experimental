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


from sqlalchemy import Column, Integer, String

from service.util.repr import make_repr_str
from .base import PyfaBase
from .func import pyfa_persist, pyfa_abandon


class Character(PyfaBase):
    """
    This class will be used for managing characters (e.g. in character
    editor). Fits will use other class' instance as character. We cannot
    use this one because different fits carry different attributes on
    character and all child entities (like skills, on-character implants,
    and so on).
    """

    __tablename__ = 'characters'

    id = Column('character_id', Integer, primary_key=True)
    alias = Column(String)

    def __init__(self, alias=''):
        self.alias = alias

    # Miscellanea public stuff
    persist = pyfa_persist
    abandon = pyfa_abandon

    # Auxiliary methods
    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
