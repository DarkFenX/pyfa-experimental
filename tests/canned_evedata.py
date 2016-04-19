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

from service.data.eve_data import *
from service.data.eve_data import make_evedata_session


def _prep_path(db_path):
    if os.path.isfile(db_path):
        os.remove(db_path)
    else:
        db_folder = os.path.dirname(db_path)
        if os.path.isdir(db_folder) is not True:
            os.makedirs(db_folder, mode=0o755)


def make_eve_canneddata(db_path):
    _prep_path(db_path)
    edb_session = make_evedata_session(db_path)

    for i in range(1, 11):
        item = EveType(id=i, name='Item {}'.format(i))
        edb_session.add(item)

    edb_session.commit()
