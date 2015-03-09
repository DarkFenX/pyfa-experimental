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


from service.data.pyfa_data.aux.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError


__all__ = [
    'SubsystemSet'
]


class SubsystemSet:
    """
    Container for subsystems.
    """

    def __init__(self, ship):
        self.__ship = ship
        self.__set = set()

    def add(self, subsystem):
        """
        Add subsystem to set.

        Required arguments:
        subsystem -- subsystem to add, cannot be None
        """
        # TODO: handle through command manager
        if subsystem._ship is not None:
            raise ItemAlreadyUsedError(subsystem)
        subsystem._ship = self.__ship
        self.__set.add(subsystem)

    def remove(self, subsystem):
        """
        Remove subsystem from set.

        Required arguments:
        subsystem -- subsystem to remove, must be one of
        subsystems from the set
        """
        # TODO: handle through command manager
        if subsystem._ship is None:
            raise ItemRemovalConsistencyError(subsystem)
        subsystem._ship = None
        self.__set.remove(subsystem)

    def clear(self):
        """
        Remove all subsystems from set.
        """
        # TODO: handle through command manager
        for subsystem in self.__set:
            if subsystem._ship is None:
                raise ItemRemovalConsistencyError(subsystem)
            subsystem._ship = None
        self.__set.clear()

    def __iter__(self):
        return self.__set.__iter__()

    def __contains__(self, subsystem):
        return self.__set.__contains__(subsystem)

    def __len__(self):
        return self.__set.__len__()

    def __repr__(self):
        return repr(self.__set)
