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

from eos import Fit as EosFit
from service.source_mgr import SourceManager, Source
from .base import PyfaBase


class Fit(PyfaBase):

    __tablename__ = 'fits'

    id = Column('fit_id', Integer, primary_key=True)
    name = Column('fit_name', String, nullable=False)
    _ship_type_id = Column('ship_type_id', Integer, nullable=False)

    def __init__(self, source, name=None):
        self.__source = None
        self.__ship = None
        self._eos_fit = EosFit()
        self.source = source
        self.name = name

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        # Attempt to fetch source from source manager if passed object
        # is not instance of source class
        if not isinstance(new_source, Source):
            new_source = SourceManager.get_source(new_source)
        if self.__source == new_source:
            return
        self.__source = new_source
        # Change eos instance on EosFit we work on; it automatically
        # propagates to all child EosFit objects
        self._eos_fit.eos = new_source.eos
        # Update source-dependent data for all child objects
        for child in (
            self.ship,
        ):
            if child is not None:
                child.update_source()

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, new_ship):
        # DB
        self._ship_type_id = new_ship.eve_id
        # Internal
        self.__ship = new_ship
        self._eos_fit.ship = new_ship._eos_ship
        # External
        new_ship._fit = self

    def __repr__(self):
        return '<Fit(id={})>'.format(self.id)

    @property
    def stats(self):
        return self._eos_fit.stats
