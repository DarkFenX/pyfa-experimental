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
from .dgmattribute import DgmAttribute
from .dgmeffect import DgmEffect
from .evegroup import EveGroup
from .evetype import EveType


def query_type(evedata_session, type_id):
    type_ = evedata_session.query(EveType).get(type_id)
    return type_


def query_types(evedata_session, type_ids):
    types = evedata_session.query(EveType).filter(EveType.id.in_(type_ids)).all()
    return types


def query_attribute(evedata_session, attribute_id):
    attribute = evedata_session.query(DgmAttribute).get(attribute_id)
    return attribute


def query_attributes(evedata_session, attribute_ids):
    attributes = evedata_session.query(DgmAttribute).filter(DgmAttribute.id.in_(attribute_ids)).all()
    return attributes


def query_effect(evedata_session, effect_id):
    effect = evedata_session.query(DgmEffect).get(effect_id)
    return effect


def query_effects(evedata_session, effect_ids):
    effects = evedata_session.query(DgmEffect).filter(DgmEffect.id.in_(effect_ids)).all()
    return effects


def query_published_skills(evedata_session):
    skills = evedata_session.query(EveType).join(EveGroup).filter(
        and_(EveGroup._category_id == ConstCategory.skill, EveType.published == True))
    return skills


__all__ = [
    'query_type',
    'query_types',
    'query_attribute',
    'query_attributes',
    'query_effect',
    'query_effects',
    'query_published_skills'
]
