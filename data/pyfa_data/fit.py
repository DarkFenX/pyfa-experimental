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


from itertools import chain

from sqlalchemy import Column, Integer, String

from eos import Fit as EosFit
from service import SourceManager, Source
from .aux import get_children
from .aux.command import CommandManager, FitSourceChangeCommand, FitShipChangeCommand
from .base import PyfaBase


class Fit(PyfaBase):

    __tablename__ = 'fits'

    id = Column('fit_id', Integer, primary_key=True)
    name = Column('fit_name', String, nullable=False)
    _ship_type_id = Column('ship_type_id', Integer, nullable=False)
    _stance_type_id = Column('stance_type_id', Integer)

    def __init__(self, source, name=None):
        # Attributes which store objects hidden by properties
        self.__source = None
        self.__ship = None
        # Eos fit will be primary point of using Eos calculation engine for
        # fit-specific data
        self._eos_fit = EosFit()
        # Manages fit-specific data needed for undo/redo
        self._cmd_mgr = CommandManager(100)
        # Set passed values
        self._set_source(source)
        self.name = name

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        command = FitSourceChangeCommand(self, new_source)
        self._cmd_mgr.do(command)

    def _set_source(self, new_source):
        # Attempt to fetch source from source manager if passed object
        # is not instance of source class
        if not isinstance(new_source, Source):
            new_source = SourceManager.get_source(new_source)
        # Do not update anything if sources are the same
        if self.source == new_source:
            return
        self.__source = new_source
        # Update eos model with new data
        self._eos_fit.eos = new_source.eos
        # Update pyfa model with new data
        for child in chain(
            (self.ship,)
        ):
            if child is None:
                continue
            child._update_source()

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, new_ship):
        command = FitShipChangeCommand(self, new_ship)
        self._cmd_mgr.do(command)

    def _set_ship(self, new_ship):
        old_ship = self.__ship
        # Clean-up
        if old_ship is not None:
            old_ship._fit = None
        # Replacements
        self.__ship = new_ship
        # Additions
        if new_ship is not None:
            new_ship._fit = self

    @property
    def _children(self):
        return get_children(chain(
            (self.ship,)
        ))

    @property
    def stats(self):
        return self._eos_fit.stats

    # Undo/redo proxies
    @property
    def has_undo(self):
        return self._cmd_mgr.has_undo

    @property
    def has_redo(self):
        return self._cmd_mgr.has_redo

    def undo(self):
        self._cmd_mgr.undo()

    def redo(self):
        self._cmd_mgr.redo()

    # Auxiliary/service stuff
    def __repr__(self):
        return '<Fit(id={})>'.format(self.id)
