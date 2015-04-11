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


from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, backref

from service.util.repr import make_repr_str
from .base import EveBase


class DgmTypeAttribute(EveBase):
    """
    Association object between type and attribute metadata, which also stores
    attribute value. Not directly accessible by pyfa.
    """

    __tablename__ = 'dgmtypeattribs'

    type_id = Column('typeID', Integer, ForeignKey('invtypes.typeID'), primary_key=True)
    type_ = relationship('InvType', backref=backref(
        '_dgmtypeattribs', collection_class=set, cascade='all, delete-orphan'))

    attribute_id = Column('attributeID', Integer, ForeignKey('dgmattribs.attributeID'), primary_key=True)
    attribute = relationship('DgmAttribute', backref=backref(
        '_dgmtypeattribs', collection_class=set, cascade='all, delete-orphan'))

    value = Column('value', Float, nullable=False)

    def __repr__(self):
        spec = ['type_id', 'attribute_id']
        return make_repr_str(self, spec)
