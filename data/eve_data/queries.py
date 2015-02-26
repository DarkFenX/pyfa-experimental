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


from .invtype import InvType
from .dgmattribute import DgmAttribute


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


__all__ = [
    'get_type',
    'get_types',
    'get_attribute',
    'get_attributes'
]
