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


from sqlalchemy import Column, ForeignKey, Integer, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from util.repr import make_repr_str
from .base import EveBase


class EveType(EveBase):
    """
    Type (aka eve item) with all its properties. Directly accessible by pyfa.
    """

    __tablename__ = 'evetypes'

    id = Column('typeID', Integer, primary_key=True)
    name = Column('typeName_en-us', String)

    _group_id = Column('groupID', Integer, ForeignKey('evegroups.groupID'))
    group = relationship('EveGroup')

    published = Column(Boolean)

    _market_group_id = Column('marketGroupID', Integer, ForeignKey('evemarketgroups.marketGroupID'))
    market_group = relationship('EveMarketGroup')

    attributes = association_proxy('_dgmtypeattribs', 'value')
    effects = association_proxy('_dgmtypeeffects', 'effect')

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
