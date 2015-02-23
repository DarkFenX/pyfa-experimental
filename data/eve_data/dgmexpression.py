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

from .base import EveBase


class DgmExpression(EveBase):

    __tablename__ = 'dgmexpressions'

    id = Column('expressionID', Integer, primary_key=True)
    operand_id = Column('operandID', Integer)
    arg1 = Column(Integer)
    arg2 = Column(Integer)
    expression_value = Column('expressionValue', String)
    expression_type_id = Column('expressionTypeID', String)
    expression_group_id = Column('expressionGroupID', String)
    expression_attribute_id = Column('expressionAttributeID', String)

    def __repr__(self):
        return '<DgmExpression(id={})>'.format(self.id)
