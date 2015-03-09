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
from .abc import BaseCommand


class ShipStanceChangeCommand(BaseCommand):

    def __init__(self, ship, new_stance):
        self.__executed = False
        self.ship = ship
        self.old_stance = ship.stance
        self.new_stance = new_stance

    def run(self):
        self.ship._set_stance(self.new_stance)
        self.__executed = True

    def reverse(self):
        self.ship._set_stance(self.old_stance)
        self.__executed = False

    @property
    def executed(self):
        return self.__executed

    def __repr__(self):
        return make_repr_str(self, ())
