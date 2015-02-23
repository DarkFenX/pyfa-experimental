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
from sqlalchemy.orm import relationship

from .base import EveBase


class InvType(EveBase):

    __tablename__ = 'invtypes'

    type_id = Column('typeID', Integer, primary_key=True)
    type_name = Column('typeName', String)

    _attrib_associations = relationship('DgmTypeAttribute')
    _effect_associations = relationship('DgmTypeEffect')

    @property
    def attributes(self):
        # Format:
        # {DgmAttribute: value}
        attribute_map = {}
        for attrib_association in self._attrib_associations:
            attribute_map[attrib_association.attribute] = attrib_association.value
        return attribute_map

    @property
    def effects(self):
        # Format:
        # {DgmEffect: is effect default for given type or not}
        effect_map = {}
        for effect_association in self._effect_associations:
            effect_map[effect_association.effect] = effect_association.is_default
        return effect_map

    def __repr__(self):
        return '<InvType(type_id={})>'.format(self.type_id)
