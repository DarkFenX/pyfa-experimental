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


from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref, reconstructor

from service.data.pyfa_data.base import PyfaBase, EveItemWrapper
from util.repr import make_repr_str


class ModuleRacks:
    """
    Higher-level container for all module racks
    (which are containers for holders).
    """

    def __init__(self):
        self.high = []
        self.med = []
        self.low = []

    def __repr__(self):
        spec = ['high', 'med', 'low']
        return make_repr_str(self, spec)


class Module(PyfaBase, EveItemWrapper):
    """
    Pyfa model: fit.modules.[high]/[med]/[low]
    Eos model: efit.modules.[high]/[med]/[low]
    DB model: fit.{_db_modules}
    """

    __tablename__ = 'modules'

    _db_id = Column('subsystem_id', Integer, primary_key=True)

    _db_fit_id = Column('fit_id', Integer, ForeignKey('fits.fit_id'), nullable=False)
    _db_fit = relationship('Fit', backref=backref(
        '_db_modules', collection_class=list, cascade='all, delete-orphan'))

    _db_type_id = Column('type_id', Integer, nullable=False)
    _db_rack_id = Column('rack_id', Integer, nullable=False)
    _db_index = Column('index', Integer, nullable=False)

    def __init__(self, type_id):
        self._db_type_id = type_id
        self.__generic_init()

    @reconstructor
    def _dbinit(self):
        self.__generic_init()

    def __generic_init(self):
        EveItemWrapper.__init__(self, self._db_type_id)
        self.__parent_ship = None
        self.__eos_module = None
