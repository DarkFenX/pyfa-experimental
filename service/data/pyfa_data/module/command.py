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


from service.data.pyfa_data.command import BaseCommand
from util.repr import make_repr_str


__all__ = [
    'ModuleEquipCommand',
]


class ModuleEquipCommand(BaseCommand):

    def __init__(self, container, module):
        self.__executed = False
        self.container = container
        self.module = module

    def run(self):
        self.container._equip_to_list(self.module)
        self.__executed = True

    def reverse(self):
        self.container._free_from_list(self.module)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())
