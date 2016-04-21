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
from service.source import SourceManager
from tests.model_structure.model_testcase import ModelTestCase


class TestModelFit(ModelTestCase):

    @patch('service.data.pyfa_data.ship.ship.EosShip')
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_fit_construction(self, eos_fit, eos_ship):
        fit = Fit(name='test fit 1')
        fit.ship = Ship(1)
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        # Reload model via persistence (DB check)
        fit.persist()
        PyfaDataManager.commit()
        del fit
        fits = query_all_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})

    @patch('service.data.pyfa_data.ship.ship.EosShip')
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_fit_src_switch(self, eos_fit, eos_ship):
        fit = Fit(name='test fit 1')
        fit.ship = Ship(1)
        # Action
        fit.source = self.source_sisi
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, self.source_sisi)
        # Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        # Reload model via persistence (DB check)
        fit.persist()
        PyfaDataManager.commit()
        del fit
        fits = query_all_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.name, 'test fit 1')
        self.assertIs(fit.source, SourceManager.default)
        # Eos model
        self.assertEqual(len(eos_fit.mock_calls), 1)
        name, args, kwargs = eos_fit.mock_calls[0]
        self.assertEqual(name, '')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
