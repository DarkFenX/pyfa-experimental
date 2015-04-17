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

from util.repr import make_repr_str
from .base import EveBase


class DgmEffect(EveBase):
    """
    Effect object with all its properties. Directly accessible by pyfa.
    """

    __tablename__ = 'dgmeffects'

    id = Column('effectID', Integer, primary_key=True)
    name = Column('effectName', String)
    _category = Column('effectCategory', Integer, nullable=False)
    _is_offensive = Column('isOffensive', Boolean, nullable=False)
    _is_assistance = Column('isAssistance', Boolean, nullable=False)
    _modifier_info = Column('modifierInfo', String)

    _pre_expression_id = Column('preExpression', Integer, ForeignKey('dgmexpressions.expressionID'))
    _pre_expression = relationship('DgmExpression', foreign_keys=_pre_expression_id)

    _post_expression_id = Column('postExpression', Integer, ForeignKey('dgmexpressions.expressionID'))
    _post_expression = relationship('DgmExpression', foreign_keys=_post_expression_id)

    _duration_attribute_id = Column('durationAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _duration_attribute = relationship('DgmAttribute', foreign_keys=_duration_attribute_id)

    _discharge_attribute_id = Column('dischargeAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _discharge_attribute = relationship('DgmAttribute', foreign_keys=_discharge_attribute_id)

    _range_attribute_id = Column('rangeAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _range_attribute = relationship('DgmAttribute', foreign_keys=_range_attribute_id)

    _falloff_attribute_id = Column('falloffAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _falloff_attribute = relationship('DgmAttribute', foreign_keys=_falloff_attribute_id)

    _tracking_speed_attribute_id = Column('trackingSpeedAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _tracking_speed_attribute = relationship('DgmAttribute', foreign_keys=_tracking_speed_attribute_id)

    _fitting_usage_chance_attribute_id = Column('fittingUsageChanceAttributeID', Integer, ForeignKey('dgmattribs.attributeID'))
    _fitting_usage_chance_attribute = relationship('DgmAttribute', foreign_keys=_fitting_usage_chance_attribute_id)

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
