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
from tests.pyfa_testcase import PyfaTestCase

from service.data.pyfa_data import PyfaDataManager
from service.source_mgr import SourceManager


class ModelTestCase(PyfaTestCase):
    """
    Additional functionality provided:

    self.fit -- precreated fit with self.ch used as cache handler
    self.assert_link_buffers_empty -- checks if link tracker buffers
    of passed fit are clear
    """

    def setUp(self):
        super().setUp()
        # Prepare EVE data
        SourceManager.add('tq', self.evedb_path_tq, make_default=True)
        SourceManager.add('sisi', self.evedb_path_sisi)
        # Prepare pyfa database
        if os.path.isfile(self.pyfadb_path):
            os.remove(self.pyfadb_path)
        PyfaDataManager.set_pyfadb_path(self.pyfadb_path)

    def tearDown(self):
        if os.path.isfile(self.pyfadb_path):
            os.remove(self.pyfadb_path)
        super().tearDown()

    @property
    def source_default(self):
        return SourceManager.default

    def pyfa_commit(self):
        PyfaDataManager.commit()
