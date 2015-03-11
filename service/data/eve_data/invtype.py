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


from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, String
from sqlalchemy.orm import Session, relationship

from service.util.repr import make_repr_str
from .base import EveBase
from .dgmattribute import DgmAttribute


BASIC_ATTRS = {
    4: '_mass',
    38: '_capacity',
    161: '_volume',
    162: '_radius'
}


class InvType(EveBase):
    """
    Type (aka eve item) with all its properties. Directly accessible by pyfa.
    """

    __tablename__ = 'invtypes'

    id = Column('typeID', Integer, primary_key=True)
    name = Column('typeName', String)
    _mass = Column('mass', Float, nullable=False)
    _capacity = Column('capacity', Float, nullable=False)
    _volume = Column('volume', Float, nullable=False)
    _radius = Column('radius', Float, nullable=False)

    _group_id = Column('groupID', Integer, ForeignKey('invgroups.groupID'))
    group = relationship('InvGroup')

    published = Column(Boolean)

    _market_group_id = Column('marketGroupID', Integer, ForeignKey('invmarketgroups.marketGroupID'))
    market_group = relationship('InvMarketGroup')


    _attrib_associations = relationship('DgmTypeAttribute')
    _effect_associations = relationship('DgmTypeEffect')

    @property
    def attributes(self):
        """
        Return attributes of type as {DgmAttribute: value} dictionary.
        """
        attribute_map = {}
        # Process basic attributes (those stored in invtypes table) first
        evedata_session = Session.object_session(self)
        for attribute in evedata_session.query(DgmAttribute).filter(DgmAttribute.id.in_(BASIC_ATTRS.keys())).all():
            attribute_map[attribute] = getattr(self, BASIC_ATTRS[attribute.id])
        # Then extended (in dgmtypeattribs table)
        for attrib_association in self._attrib_associations:
            attribute_map[attrib_association.attribute] = attrib_association.value
        return attribute_map

    @property
    def effects(self):
        """
        Return effects of type as DgmEffect list.
        """
        return [assoc.effect for assoc in self._effect_associations]

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
