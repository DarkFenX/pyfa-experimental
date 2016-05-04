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


from unittest.mock import call

from service.data.pyfa_data import *
from tests.model_structure.model_testcase import ModelTestCase


class TestModelSubsystemCoupledRemove(ModelTestCase):

    def test_do(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        subsystem = Subsystem(4)
        ship.subsystems.add(subsystem)
        fit.ship = ship
        fit.purge_commands()
        # Action (removing with parent from fit)
        fit.ship = None
        # Pyfa model
        self.assertIs(ship.stance, stance)
        self.assertEqual(stance.eve_id, 5)
        self.assertIs(stance.eve_name, None)
        # Eos model
        self.assertIs(fit._eos_fit.stance, None)
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
        self.assertIs(fit.ship, None)
        # Eos model
        self.assertIs(fit._eos_fit.stance, None)
        # Action (removing from detached parent)
        ship.stance = None
        # Pyfa model
        self.assertIs(ship.stance, None)
        self.assertEqual(stance.eve_id, 5)
        self.assertIs(stance.eve_name, None)

    def test_do(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        subsystem = Subsystem(4)
        # Action (adding to detached parent)
        ship.subsystems.add(subsystem)
        # Pyfa model
        self.assertEqual(len(ship.subsystems), 1)
        self.assertIn(subsystem, ship.subsystems)
        self.assertEqual(subsystem.eve_id, 4)
        self.assertIs(subsystem.eve_name, None)
        # Action (adding with parent to fit)
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        fit.ship = ship
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(ship.subsystems), 1)
        self.assertIn(subsystem, ship.subsystems)
        self.assertEqual(subsystem.eve_id, 4)
        self.assertEqual(subsystem.eve_name, 'Item 4 (TQ)')
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.add(subsystem._eos_item))
        # Command queue
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.ship.subsystems), 1)
        subsystem = next(iter(fit.ship.subsystems))
        self.assertEqual(subsystem.eve_id, 4)
        self.assertEqual(subsystem.eve_name, 'Item 4 (TQ)')
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.add(subsystem._eos_item))

    def test_undo(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        subsystem = Subsystem(4)
        ship.subsystems.add(subsystem)
        fit.ship = ship
        # Action
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        fit.undo()
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(ship.subsystems), 1)
        self.assertIn(subsystem, ship.subsystems)
        self.assertEqual(subsystem.eve_id, 4)
        self.assertIs(subsystem.eve_name, None)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.remove(subsystem._eos_item))
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, True)
        # Reload model via persistence (DB check)
        fit.persist()
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertIs(fit.ship, None)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 0)

    def test_redo(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        subsystem = Subsystem(4)
        ship.subsystems.add(subsystem)
        fit.ship = ship
        fit.undo()
        # Action
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        fit.redo()
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(ship.subsystems), 1)
        self.assertIn(subsystem, ship.subsystems)
        self.assertEqual(subsystem.eve_id, 4)
        self.assertEqual(subsystem.eve_name, 'Item 4 (TQ)')
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.add(subsystem._eos_item))
        # Command queue
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.ship.subsystems), 1)
        subsystem = next(iter(fit.ship.subsystems))
        self.assertEqual(subsystem.eve_id, 4)
        self.assertEqual(subsystem.eve_name, 'Item 4 (TQ)')
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.add(subsystem._eos_item))
