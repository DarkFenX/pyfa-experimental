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


from sqlalchemy import Column, String

from service.util.repr import make_repr_str
from .base import EveBase


class PhbMetaData(EveBase):
    """
    EVE database metadata (like client version). Directly accessible by pyfa.
    """

    __tablename__ = 'phbmetadata'

    field_name = Column(String, primary_key=True)
    field_value = Column(String)

    def __repr__(self):
        spec = ['field_name']
        return make_repr_str(self, spec)
