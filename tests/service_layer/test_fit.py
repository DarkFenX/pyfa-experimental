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
from unittest.mock import patch

from service.data.pyfa_data import *
from service.data.pyfa_data import PyfaDataManager
from service.data.pyfa_data.query import *
from service.source_mgr import SourceManager
from tests.pyfa_testcase import PyfaTestCase


class TestPyfaService(PyfaTestCase):


    @patch('service.data.pyfa_data.ship.ship.EosShip')
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    @patch('service.source_mgr.EosSourceManager')
    def test_fit(self, eos_srcmgr, eos_fit, eos_ship):
        # Prep steps
        test_dir = os.path.dirname(os.path.abspath(__file__))
        eve_dbpath = os.path.join(test_dir, '..', '..', 'staticdata', 'canned.db')
        pyfa_dbpath = os.path.join(test_dir, 'pyfadata.db')

        SourceManager.add('tq', eve_dbpath, make_default=True)

        if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
        PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
        fit = Fit(name='test fit 1')
        fit.ship = Ship(1)  # Assign ship just because we have to, there can be no fit w/o ship

        # Checking Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Checking Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        # Checking DB model (via persistence check)
        fit.persist()
        PyfaDataManager.commit()
        del fit
        fits = query_all_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Checking Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Checking Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})


    @patch('service.data.pyfa_data.ship.ship.EosShip')
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    @patch('service.source_mgr.EosSourceManager')
    def test_ship(self, eos_srcmgr, eos_fit, eos_ship):
        # Prep steps
        test_dir = os.path.dirname(os.path.abspath(__file__))
        eve_dbpath = os.path.join(test_dir, '..', '..', 'staticdata', 'canned.db')
        pyfa_dbpath = os.path.join(test_dir, 'pyfadata.db')

        SourceManager.add('tq', eve_dbpath, make_default=True)

        if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
        PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        fit.ship = ship
        # Checking Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Checking Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        # Checking DB model (via persistence check)
        fit.persist()
        PyfaDataManager.commit()
        del fit
        fits = query_all_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Checking Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Checking Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
