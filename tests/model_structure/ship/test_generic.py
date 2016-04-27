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


from unittest.mock import patch, call, sentinel

from service.data.pyfa_data import *
from service.data.pyfa_data.ship.ship import EosShip
from tests.model_structure.model_testcase import ModelTestCase


class TestModelShipGeneric(ModelTestCase):

    @patch('service.data.pyfa_data.ship.ship.EosShip', spec=EosShip)
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_instantiation(self, eos_fit, eos_ship):
        eos_ship.side_effect = [sentinel.eship_old, sentinel.eship_new]
        ship_old = Ship(1)
        fit = Fit(name='test fit 1', ship=ship_old)
        eship_calls_before = len(eos_ship.mock_calls)
        ship_new = Ship(7)
        eship_calls_after = len(eos_ship.mock_calls)
        # Pyfa model
        self.assertEqual(ship_new.eve_id, 7)
        self.assertIs(ship_new.eve_name, None)
        # Eos model
        self.assertEqual(eship_calls_after - eship_calls_before, 1)
        self.assertEqual(eos_ship.mock_calls[-1], call(7))
        self.assertIs(ship_new._eos_item, sentinel.eship_new)
        self.assertIs(fit._eos_fit.ship, sentinel.eship_old)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)

    @patch('service.data.pyfa_data.ship.ship.EosShip', spec=EosShip)
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_persistence(self, eos_fit, eos_ship):
        eos_ship.return_value = sentinel.eship
        ship = Ship(1)
        fit = Fit(name='test fit 1', ship=ship)
        # Reload model via persistence (DB check)
        fit.persist()
        eship_calls_before = len(eos_ship.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        eship_calls_after = len(eos_ship.mock_calls)
        # Pyfa model
        self.assertEqual(fit.ship.eve_id, 1)
        self.assertEqual(fit.ship.eve_name, 'Item 1 (TQ)')
        # Eos model
        self.assertEqual(eship_calls_after - eship_calls_before, 1)
        self.assertEqual(eos_ship.mock_calls[-1], call(1))
        self.assertIs(fit._eos_fit.ship, sentinel.eship)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
