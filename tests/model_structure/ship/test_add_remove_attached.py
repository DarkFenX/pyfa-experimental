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


from unittest.mock import patch

from service.data.pyfa_data import *
from service.data.pyfa_data.ship.ship import EosShip
from tests.model_structure.model_testcase import ModelTestCase


class TestModelShipAddRemoveAttached(ModelTestCase):

    @patch('service.data.pyfa_data.ship.ship.EosShip', spec=EosShip)
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_do(self, eos_fit, eos_ship):
        ship_old = Ship(1)
        fit = Fit(name='test fit 1', ship=ship_old)
        ship_new = Ship(7)
        # Action
        fit.ship = ship_new
        # Pyfa model
        self.assertIs(fit.ship, ship_new)
        self.assertEqual(ship_old.eve_id, 1)
        self.assertIs(ship_old.eve_name, None)
        self.assertEqual(ship_new.eve_id, 7)
        self.assertEqual(ship_new.eve_name, 'Item 7 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)
        # Command queue
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.ship.eve_id, 7)
        self.assertEqual(fit.ship.eve_name, 'Item 7 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)


    @patch('service.data.pyfa_data.ship.ship.EosShip', spec=EosShip)
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_undo(self, eos_fit, eos_ship):
        ship_old = Ship(1)
        fit = Fit(name='test fit 1', ship=ship_old)
        ship_new = Ship(7)
        fit.ship = ship_new
        # Action
        fit.undo()
        # Pyfa model
        self.assertIs(fit.ship, ship_old)
        self.assertEqual(ship_old.eve_id, 1)
        self.assertEqual(ship_old.eve_name, 'Item 1 (TQ)')
        self.assertEqual(ship_new.eve_id, 7)
        self.assertIs(ship_new.eve_name, None)
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, True)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.ship.eve_id, 1)
        self.assertEqual(fit.ship.eve_name, 'Item 1 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)


    @patch('service.data.pyfa_data.ship.ship.EosShip', spec=EosShip)
    @patch('service.data.pyfa_data.fit.fit.EosFit')
    def test_redo(self, eos_fit, eos_ship):
        ship_old = Ship(1)
        fit = Fit(name='test fit 1', ship=ship_old)
        ship_new = Ship(7)
        fit.ship = ship_new
        fit.undo()
        # Action
        fit.redo()
        # Pyfa model
        self.assertIs(fit.ship, ship_new)
        self.assertEqual(ship_old.eve_id, 1)
        self.assertIs(ship_old.eve_name, None)
        self.assertEqual(ship_new.eve_id, 7)
        self.assertEqual(ship_new.eve_name, 'Item 7 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)
        # Command queue
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.ship.eve_id, 7)
        self.assertEqual(fit.ship.eve_name, 'Item 7 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.ship, fit.ship._eos_item)
