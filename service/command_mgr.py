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


class CommandManager:
    """
    Class which handles undo/redo activities on objects
    which need them.

    Requred arguments:
    capacity -- capacity of undo/redo queues
    """

    def __init__(self, capacity):
        self._capacity = capacity
        # [earlier action, later action]
        self._undos = []
        # [later action, earlier action]
        self._redos = []

    def do(self, command):
        self._redos.clear()
        command.run()
        self._limited_append(self._undos, command)

    def undo(self):
        try:
            command = self._undos.pop(-1)
        except IndexError:
            return
        command.reverse()
        self._limited_append(self._redos, command)

    def redo(self):
        try:
            command = self._redos.pop(-1)
        except IndexError:
            return
        command.run()
        self._limited_append(self._undos, command)

    def _limited_append(self, container, command):
        """
        Append element to the list, not allowing length of list
        to exceed the capacity.
        """
        container.append(command)
        if len(container) > self._capacity:
            del container[:len(container) - self._capacity]

    @property
    def has_undo(self):
        """
        Check if there're any actions in undo queue.
        """
        return bool(self._undos)

    @property
    def has_redo(self):
        """
        Check if there're any actions in redo queue.
        """
        return bool(self._redos)


class BaseCommand(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def reverse(self):
        ...
