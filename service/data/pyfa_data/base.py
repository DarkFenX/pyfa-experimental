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


from abc import ABCMeta, abstractmethod

from sqlalchemy.ext.declarative import declarative_base

from service.data.eve_data.query import query_type, query_attributes

PyfaBase = declarative_base()


class FitItemBase(metaclass=ABCMeta):
    """
    Defines interface for all objects which represent
    EVE items in pyfa model.
    """

    def __init__(self, type_id):
        self._type_id = type_id
        self._eve_item = None

    @property
    def eve_id(self):
        """
        Return type ID of EVE item, even if source is not defined.
        """
        return self._type_id

    @property
    def eve_name(self):
        """
        Return name of EVE item, if source is defined. If source
        is not defined, return None.
        """
        try:
            return self._eve_item.name
        except AttributeError:
            return None

    @property
    def attributes(self):
        """
        Return dictionary with modified attributes in the form of
        {DgmAttribute: attr value}. If source is not defined,
        return empty dictionary.
        """
        try:
            edb_session = self._source.edb
        except AttributeError:
            return {}
        eos_attrs = self._eos_item.attributes
        attr_ids = eos_attrs.keys()
        attrs = query_attributes(edb_session, attr_ids)
        attr_map = {}
        for attr in attrs:
            attr_map[attr] = eos_attrs[attr.id]
        return attr_map


    @property
    def attributes_original(self):
        """
        Return dictionary with original attributes in the form of
        {DgmAttribute: attr value}. If source is not defined,
        return empty dictionary.
        """
        try:
            return self._eve_item.attributes
        except AttributeError:
            return {}

    @property
    def effects(self):
        """
        Return set with item effects. If source is not defined,
        return empty set.
        """
        try:
            return self._eve_item.effects
        except AttributeError:
            return set()

    def _update_source(self):
        try:
            edb_session = self._source.edb
        except AttributeError:
            self._eve_item = None
        else:
            self._eve_item = query_type(edb_session, self.eve_id)

    @property
    @abstractmethod
    def _source(self):
        ...

    @property
    @abstractmethod
    def _eos_item(self):
        ...

    @abstractmethod
    def _src_children(self):
        ...
