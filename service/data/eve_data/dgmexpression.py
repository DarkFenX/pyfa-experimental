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


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from util.repr import make_repr_str
from .base import EveBase


class DgmExpression(EveBase):
    """
    Effect expression object with all its properties. Is not accessible by pyfa.
    """

    __tablename__ = 'dgmexpressions'

    id = Column('expressionID', Integer, primary_key=True)
    operand_id = Column('operandID', Integer, nullable=False)

    _arg1_id = Column('arg1', Integer, ForeignKey('dgmexpressions.expressionID'))
    arg1 = relationship('DgmExpression', foreign_keys=_arg1_id)

    _arg2_id = Column('arg2', Integer, ForeignKey('dgmexpressions.expressionID'))
    arg2 = relationship('DgmExpression', foreign_keys=_arg2_id)

    expression_value = Column('expressionValue', String)

    _expression_type_id = Column('expressionTypeID', Integer, ForeignKey('invtypes.typeID'))
    expression_type = relationship('InvType')

    _expression_group_id = Column('expressionGroupID', Integer, ForeignKey('invgroups.groupID'))
    expression_group = relationship('InvGroup')

    _expression_attribute_id = Column('expressionAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    expression_attribute = relationship('DgmAttribute')

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
