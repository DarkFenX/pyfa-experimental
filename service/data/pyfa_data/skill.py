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

from service.util.repr import make_repr_str
from .base import PyfaBase
from .func import pyfa_persist, pyfa_abandon


class Skill(PyfaBase):
    """
    This class will be used for managing character's skills (like for character
    editor). Fits will use other class instances as skills to carry attributes.
    """

    __tablename__ = 'skills'

    id = Column('skill_id', Integer, primary_key=True)

    _character_id = Column('character_id', Integer, ForeignKey('characters.character_id'), nullable=False)
    _character = relationship('Character', backref=backref(
        'skills', collection_class=set, cascade='all, delete-orphan'))

    eve_id = Column('type_id', Integer, nullable=False)
    level = Column(Integer, nullable=False)


    def __init__(self, type_id, level=0):
        self.eve_id = type_id
        self.level = level

    # Auxiliary methods
    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
