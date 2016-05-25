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
from util.repr import make_repr_str
from .command import *


__all__ = [
    'SubsystemSet'
]


class ModuleRacks:
    """
    Higher-level container for all module racks
    (which are containers for holders).
    """

    def __init__(self):
        self.high = []
        self.med = []
        self.low = []

    def __repr__(self):
        spec = ['high', 'med', 'low']
        return make_repr_str(self, spec)


class ModuleList:
    """
    Container for modules.
    """

    def __init__(self, ship):
        self.__parent_ship = ship
        self.__list = []

    def add(self, module):
        """
        Append module to the end of rack.

        Required arguments:
        module -- module to append, cannot be None
        """
        command = ModuleAppendCommand(self, module)
        try:
            cmd_mgr = self.__parent_ship._parent_fit._cmd_mgr
        except AttributeError:
            command.run()
        else:
            cmd_mgr.do(command)

    def _append_to_list(self, module):
        if module._parent_ship is not None:
            raise ItemAlreadyUsedError(module)
        module._parent_ship = self.__parent_ship
        self.__list.append(module)

    def remove(self, module):
        """
        Remove module from the rack.

        Required arguments:
        module -- module to remove, must be one of
        modules from the rack
        """
        command = SubsystemRemoveCommand(self, subsystem)
        try:
            cmd_mgr = self.__parent_ship._parent_fit._cmd_mgr
        except AttributeError:
            command.run()
        else:
            cmd_mgr.do(command)

    def _remove_from_list(self, module):
        if module._parent_ship is not self.__parent_ship:
            raise ItemRemovalConsistencyError(module)
        module._parent_ship = None
        self.__list.remove(module)

    def __iter__(self):
        return self.__list.__iter__()

    def __contains__(self, module):
        return self.__list.__contains__(module)

    def __len__(self):
        return self.__list.__len__()

    def __repr__(self):
        return repr(self.__list)
