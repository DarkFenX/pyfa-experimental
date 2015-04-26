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


class RestrictedSet:
    """
    Provides same interface as regular set, but with getitem
    and delitem (using item EVE ID as key) on top of that.
    Several items with the same EVE ID cannot be added to
    this set.
    """

    __emulates__ = set

    def __init__(self):
        self.__set = set()
        self.__eve_id_map = {}

    def add(self, item):
        eve_id = item.eve_id
        if eve_id in self.__eve_id_map:
            msg = 'item with EVE ID {} already exists in this set'.format(eve_id)
            raise ValueError(msg)
        self.__set.add(item)
        self.__eve_id_map[eve_id] = item

    def remove(self, item):
        if item not in self.__set:
            raise KeyError(item)
        self.__set.remove(item)
        del self.__eve_id_map[item.eve_id]

    def clear(self):
        self.__set.clear()
        self.__eve_id_map.clear()

    def __getitem__(self, eve_id):
        return self.__eve_id_map[eve_id]

    def __delitem__(self, eve_id):
        item = self.__eve_id_map[eve_id]
        self.remove(item)

    def __iter__(self):
        return self.__set.__iter__()

    def __contains__(self, holder):
        return self.__set.__contains__(holder)

    def __len__(self):
        return self.__set.__len__()

    def __repr__(self):
        return repr(self.__set)
