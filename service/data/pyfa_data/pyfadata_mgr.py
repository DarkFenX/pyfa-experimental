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


import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .base import PyfaBase


class PyfaDataManager:
    """
    Generates and holds access to pyfa database session (fits, characters, etc.)
    """

    session = None

    @classmethod
    def set_pyfadb_path(cls, pyfadb_path):
        pyfadb_folder = os.path.dirname(pyfadb_path)
        if os.path.isdir(pyfadb_folder) is not True:
            os.makedirs(pyfadb_folder, mode=0o755)
        pyfadb_engine = sqlalchemy.create_engine('sqlite:///{}'.format(pyfadb_path), echo=False)
        PyfaBase.metadata.create_all(pyfadb_engine)
        cls.session = sessionmaker(bind=pyfadb_engine)()

    @classmethod
    def commit(cls):
        cls.session.commit()
