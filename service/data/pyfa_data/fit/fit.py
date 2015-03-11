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
from sqlalchemy.orm import reconstructor

from eos import Fit as EosFit
from service.source_mgr import SourceManager, Source
from service.data.pyfa_data import Ship, Stance
from service.data.pyfa_data.command import CommandManager
from service.data.pyfa_data.exception import ItemAlreadyUsedError, ItemRemovalConsistencyError
from service.data.pyfa_data.func import get_src_children, pyfa_persist, pyfa_abandon
from service.data.pyfa_data.base import PyfaBase
from service.util.repr import make_repr_str
from .command import *


class Fit(PyfaBase):
    """
    Pyfa model children:
      .ship
    """

    __tablename__ = 'fits'

    id = Column('fit_id', Integer, primary_key=True)
    name = Column('fit_name', String, nullable=False)
    _ship_type_id = Column('ship_type_id', Integer, nullable=False)
    _stance_type_id = Column('stance_type_id', Integer)

    def __init__(self, name='', source=None):
        self.__generic_init()
        # Use default source, unless specified otherwise
        if source is None:
            source = SourceManager.default
        self._set_source(source)
        self.name = name

    @reconstructor
    def _dbinit(self):
        self.__generic_init()
        # Use default source for all reconstructed fits
        self._set_source(SourceManager.default)
        # Restore entities which are stored on fit
        self._set_ship(Ship(self._ship_type_id))
        if self._stance_type_id is not None:
            self.ship._set_stance(Stance(self._stance_type_id))
        for subsystem in self._subsystems:
            self.ship.subsystems._add_to_set(subsystem)

    def __generic_init(self):
        # Attributes which store objects hidden behind properties
        self.__source = None
        self.__ship = None
        # Eos fit will be primary point of using Eos calculation engine for
        # fit-specific data
        self._eos_fit = EosFit()
        # Manages fit-specific data needed for undo/redo
        self._cmd_mgr = CommandManager(100)

    # Read-only info
    @property
    def stats(self):
        return self._eos_fit.stats

    # Children getters/setters
    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, new_ship):
        command = FitShipChangeCommand(self, new_ship)
        self._cmd_mgr.do(command)

    def _set_ship(self, new_ship):
        old_ship = self.__ship
        if new_ship is old_ship:
            return
        if old_ship is not None:
            if old_ship._fit is None:
                raise ItemRemovalConsistencyError(old_ship)
            old_ship._fit = None
        self.__ship = new_ship
        if new_ship is not None:
            if new_ship._fit is not None:
                raise ItemAlreadyUsedError(new_ship)
            new_ship._fit = self

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

    # Miscellanea public stuff
    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, new_source):
        command = FitSourceChangeCommand(self, new_source)
        self._cmd_mgr.do(command)

    def _set_source(self, new_source):
        """
        Set fit's source. Source represents EVE data to be used.

        Required arguments:
        new_source -- source to use, can be None
        """
        # Attempt to fetch source from source manager if passed object
        # is not instance of source class
        if not isinstance(new_source, Source) and new_source is not None:
            new_source = SourceManager.get(new_source)
        old_source = self.source
        # Do not update anything if sources are the same
        if new_source is old_source:
            return
        self.__source = new_source
        # Update eos model with new data
        self._eos_fit.eos = getattr(new_source, 'eos', None)
        # Update pyfa model with new data
        for src_child in self._src_children:
            src_child._update_source()

    persist = pyfa_persist
    abandon = pyfa_abandon

    def validate(self):
        self._eos_fit.validate()

    # Auxiliary methods
    @property
    def _src_children(self):
        return get_src_children(chain(
            (self.ship,)
        ))

    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
