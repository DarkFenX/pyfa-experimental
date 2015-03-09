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
from sqlalchemy.orm import relationship

from eos import Subsystem as EosSubsystem
from service.data.eve_data.queries import get_type, get_attributes
from service.util.repr import make_repr_str
from .base import PyfaBase


class Subsystem(PyfaBase):
    """
    Pyfa model: ship.{subsystems}
    Eos model: efit.{subsystems}
    DB model: fit.{_subsystems}
    """

    __tablename__ = 'subsystems'

    _id = Column('id', Integer, primary_key=True)

    _fit_db_id = Column('fit_id', Integer, ForeignKey('fits.fit_id'))
    _fit_db = relationship('Fit', backref='_subsystems')

    _type_id = Column('type_id', Integer, nullable=False)

    def __init__(self, type_id):
        self._type_id = type_id
        self._eve_item = None
        self._eos_subsystem = EosSubsystem(type_id)

    # Read-only info
    @property
    def eve_id(self):
        return self._type_id

    @property
    def eve_name(self):
        return self._eve_item.name

    @property
    def attributes(self):
        eos_attrs = self._eos_subsystem.attributes
        attr_ids = eos_attrs.keys()
        attrs = get_attributes(self._ship._fit.source.edb, attr_ids)
        attr_map = {}
        for attr in attrs:
            attr_map[attr] = eos_attrs[attr.id]
        return attr_map

    @property
    def effects(self):
        return list(self._eve_item.effects)

    # Auxiliary methods
    # SHIP SETTERS GO INTO HERE

    def _update_source(self):
        try:
            source = self._ship._fit.source
        except AttributeError:
            self._eve_item = None
        else:
            self._eve_item = get_type(source.edb, self.eve_id)

    def __repr__(self):
        spec = ['eve_id']
        return make_repr_str(self, spec)
