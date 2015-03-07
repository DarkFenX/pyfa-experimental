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
from service import SourceManager, Source, CommandManager
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
        # Holds all child objects of fit which may need update when we change
        # source, so we can iterate through them as needed
        self._src_children = set()
        # Eos fit will be primary point of using Eos calculation engine for
        # fit-specific data
        self._eos_fit = EosFit()
        # Manages fit-specific data needed for undo/redo
        self._cmd_mgr = CommandManager(100)
        # Set passed values
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
        # Avoid any updates if they're not going to do anything
        if self.__source == new_source:
            return
        self.__source = new_source
        # Change eos instance on EosFit we work on; it automatically
        # propagates to all child EosFit objects
        self._eos_fit.eos = new_source.eos
        # Update source-dependent data for all child objects
        for child in self._src_children:
            child.update_source()

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, new_ship):
        old_ship = self.__ship
        # Clean-up
        if old_ship is not None:
            self._src_children.remove(old_ship)
            old_ship._fit = None
            if old_ship.stance is not None:
                self._stance_type_id = None
                self._eos_fit.stance = None
                self._src_children.remove(old_ship.stance)
        # Replacements
        self._ship_type_id = new_ship.eve_id
        self._eos_fit.ship = new_ship._eos_ship
        self.__ship = new_ship
        # Additions
        if new_ship is not None:
            self._src_children.add(new_ship)
            new_ship._fit = self
            if new_ship.stance is not None:
                self._stance_type_id = new_ship.stance.eve_id
                self._eos_fit.stance = new_ship.stance._eos_stance
                self._src_children.add(new_ship.stance)

    @property
    def stats(self):
        return self._eos_fit.stats

    # Undo/redo proxy methods
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
