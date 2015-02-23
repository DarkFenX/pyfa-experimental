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


from data.pyfa_data import make_pyfadata_session
from service import SourceManager


eve_sources = SourceManager.getinst()


pyfadb_session = None


def set_pyfadb_path(pyfadb_path):
    """
    Create session to SQLite database stored at path passed as
    argument, and store it as module-level pyfadb_session variable.
    """
    global pyfadb_session
    pyfadb_session = make_pyfadata_session(pyfadb_path)