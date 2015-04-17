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


from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship, backref

from util.repr import make_repr_str
from .base import EveBase


class DgmTypeEffect(EveBase):
    """
    Association object between type and effect metadata, which also stores
    if effect is default for item or not. Not directly accessible by pyfa.
    """

    __tablename__ = 'dgmtypeeffects'

    type_id = Column('typeID', Integer, ForeignKey('invtypes.typeID'), primary_key=True)
    type_ = relationship('InvType', backref=backref(
        '_dgmtypeeffects', collection_class=set, cascade='all, delete-orphan'))

    effect_id = Column('effectID', Integer, ForeignKey('dgmeffects.effectID'), primary_key=True)
    effect = relationship('DgmEffect', backref=backref(
        '_dgmtypeeffects', collection_class=set, cascade='all, delete-orphan'))

    is_default = Column('isDefault', Boolean, nullable=False)

    def __repr__(self):
        spec = ['type_id', 'effect_id']
        return make_repr_str(self, spec)
