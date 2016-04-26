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
from unittest.mock import Mock, patch, sentinel

from service.data.pyfa_data import PyfaDataManager
from service.data.pyfa_data.query import *
from service.source import SourceManager


class ModelTestCase(PyfaTestCase):
    """
    Additional functionality provided:

    Provides setup and cleanup for:
      two pyfa sources (default TQ and secondary SiSi)
      pyfa data session, to not let data persist between tests

    self.pyfadb_force_reload -- reinitializes access to pyfa db
    self.query_fits -- return list of fits currently in session
    self.source_tq -- primary pyfa source
    self.source_sisi -- secondary pyfa source
    self.eos_src_tq -- mock which is used as TQ eos source
    self.eos_src_sisi -- mock which is used as SiSi eos source

    We need last two because mock_calls do not support __setattr__,
    and we set eos source via property setter. To check it, we need
    some values to compare against, and these mocks are the values.
    """

    @patch('service.source.EosSourceManager')
    def setUp(self, eos_srcman):
        super().setUp()
        # Prepare EVE data
        self.eos_source_tq = sentinel.eos_source_tq
        self.eos_source_sisi = sentinel.eos_source_sisi
        eos_srcman.get.side_effect = lambda alias: {'tq': self.eos_source_tq, 'sisi': self.eos_source_sisi}[alias]
        SourceManager.add('tq', self.evedb_path_tq, make_default=True)
        SourceManager.add('sisi', self.evedb_path_sisi)
        # Prepare pyfa database
        self.__remove_pyfa_db()
        PyfaDataManager.set_pyfadb_path(self.pyfadb_path)

    @patch('service.source.EosSourceManager')
    def tearDown(self, eos_srcman):
        # Clean up pyfa database
        PyfaDataManager.commit()
        PyfaDataManager.close_session()
        self.__remove_pyfa_db()
        # Clean up EVE data
        SourceManager.remove('tq')
        SourceManager.remove('sisi')
        super().tearDown()

    def pyfadb_force_reload(self):
        """
        Commit current changes, and recreate session. Should be
        used to run persistence checks.
        """
        PyfaDataManager.commit()
        PyfaDataManager.close_session()
        PyfaDataManager.set_pyfadb_path(self.pyfadb_path)

    def query_fits(self):
        return query_all_fits()

    def __remove_pyfa_db(self):
        if os.path.isfile(self.pyfadb_path):
            os.remove(self.pyfadb_path)

    @property
    def source_tq(self):
        return SourceManager.get('tq')

    @property
    def source_sisi(self):
        return SourceManager.get('sisi')
