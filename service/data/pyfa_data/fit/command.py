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


from service.util.repr import make_repr_str
from service.data.pyfa_data.aux.command import BaseCommand


__all__ = [
    'FitShipChangeCommand',
    'FitSourceChangeCommand'
]


class FitShipChangeCommand(BaseCommand):

    def __init__(self, fit, new_ship):
        self.__executed = False
        self.fit = fit
        self.old_ship = fit.ship
        self.new_ship = new_ship

    def run(self):
        self.fit._set_ship(self.new_ship)
        self.__executed = True

    def reverse(self):
        self.fit._set_ship(self.old_ship)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())


class FitSourceChangeCommand(BaseCommand):

    def __init__(self, fit, new_source):
        self.__executed = False
        self.fit = fit
        self.old_source = fit.source
        self.new_source = new_source

    def run(self):
        self.fit._set_source(self.new_source)
        self.__executed = True

    def reverse(self):
        self.fit._set_source(self.old_source)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())
