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


from service.data.pyfa_data.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError
from util.const import RackType
from util.repr import make_repr_str
from .command import *


pyfa_rack_map = {
    RackType.high: 'high',
    RackType.med: 'med',
    RackType.low: 'low'
}


class ModuleRacks:
    """
    Higher-level container for all module racks
    (which are containers for holders).
    """

    def __init__(self, ship):
        self.high = ModuleList(ship, RackType.high)
        self.med = ModuleList(ship, RackType.med)
        self.low = ModuleList(ship, RackType.low)

    def __repr__(self):
        spec = ['high', 'med', 'low']
        return make_repr_str(self, spec)


class ModuleList:
    """
    Container for modules.
    """

    def __init__(self, ship, rack_type):
        self.__parent_ship = ship
        self.__rack_type = rack_type
        self.__list = []

    # Adding modules
    def equip(self, module):
        """
        Put module to first free slot in container; if
        container doesn't have free slots, append holder
        to the end of container.
        """
        command = ModuleEquipCommand(self, module)
        try:
            cmd_mgr = self.__parent_ship._parent_fit._cmd_mgr
        except AttributeError:
            command.run()
        else:
            cmd_mgr.do(command)

    def _equip_to_list(self, module):
        if module._parent_ship is not None:
            raise ItemAlreadyUsedError(module)
        try:
            index = self.__list.index(None)
        except ValueError:
            index = len(self.__list)
            self.__list.append(module)
        else:
            self.__list[index] = module
        module._set_position(self.__rack_type, index)
        module._parent_ship = self.__parent_ship

    def place(self, index, module):
        return

    def insert(self, index, module):
        return

    # Moving modules
    def swap(self, module1, module2):
        return

    def move(self, module, index):
        return

    # Removing modules
    def free(self, value):
        """
        Clear slot at specified location.

        Required arguments:
        value -- either index or module
        """
        command = ModuleFreeCommand(self, value)
        try:
            cmd_mgr = self.__parent_ship._parent_fit._cmd_mgr
        except AttributeError:
            command.run()
        else:
            cmd_mgr.do(command)

    def _free_from_list(self, value):
        if isinstance(value, int):
            index = value
            module = self.__list[index]
        else:
            module = value
            index = self.__list.index(module)
        if module is None:
            return index, module
        if module._parent_ship is not self.__parent_ship:
            raise ItemRemovalConsistencyError(module)
        module._parent_ship = None
        module._set_position(None, None)
        return index, module

    def remove(self, module):
        return

    # Special
    def __iter__(self):
        return self.__list.__iter__()

    def __contains__(self, module):
        return self.__list.__contains__(module)

    def __len__(self):
        return self.__list.__len__()

    def __repr__(self):
        return repr(self.__list)
