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


from sqlalchemy import Column, Integer, String

from .base import PyfaBase


class Fit(PyfaBase):

    # Database-related section
    __tablename__ = 'fits'
    id = Column('fit_id', Integer, primary_key=True)
    name = Column('fit_name', String, nullable=False)
    _ship_type_id = Column('ship_type_id', String, nullable=False)

    def __init__(self, source, name=None):
        super().__init__()
        self._source = source
        self._ship = None
        self.name = name

    def change_source(self, new_source):
        """
        Change source of the fit (e.g. if we have fit which is
        using tranquility data and want to see it with singularity
        data instead).

        Required arguments:
        new_source -- alias of source to use
        """
        if self._source == new_source:
            return
        self._source = new_source

    @property
    def ship(self):
        return self._ship

    @ship.setter
    def ship(self, new_ship):
        self._ship_type_id = new_ship.eve_id
        self._ship = new_ship

    @ship.deleter
    def ship(self):
        self._ship_type_id = None
        self._ship = None

    def __repr__(self):
        return '<Fit(id={})>'.format(self.id)
