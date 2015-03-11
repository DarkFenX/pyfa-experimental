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


from sqlalchemy import and_

from eos.const.eve import Category as ConstCategory
from .invgroup import InvGroup
from .invtype import InvType
from .dgmattribute import DgmAttribute
from .dgmeffect import DgmEffect


def get_type(evedata_session, type_id):
    type_ = evedata_session.query(InvType).get(type_id)
    return type_


def get_types(evedata_session, type_ids):
    types = evedata_session.query(InvType).filter(InvType.id.in_(type_ids)).all()
    return types


def get_attribute(evedata_session, attribute_id):
    attribute = evedata_session.query(DgmAttribute).get(attribute_id)
    return attribute


def get_attributes(evedata_session, attribute_ids):
    attributes = evedata_session.query(DgmAttribute).filter(DgmAttribute.id.in_(attribute_ids)).all()
    return attributes


def get_effect(evedata_session, effect_id):
    effect = evedata_session.query(DgmEffect).get(effect_id)
    return effect


def get_effects(evedata_session, effect_ids):
    effects = evedata_session.query(DgmEffect).filter(DgmEffect.id.in_(effect_ids)).all()
    return effects


def get_published_skills(evedata_session):
    skills = evedata_session.query(InvType).join(InvGroup).filter(
        and_(InvGroup._category_id == ConstCategory.skill, InvType.published == True))
    return skills


__all__ = [
    'get_type',
    'get_types',
    'get_attribute',
    'get_attributes',
    'get_effect',
    'get_effects',
    'get_published_skills'
]
