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


from service.data.pyfa_data import *
from tests.model_structure.model_testcase import ModelTestCase


class TestModelShipCoupledRemoved(ModelTestCase):

    def test_do(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        stance = Stance(5)
        ship.stance = stance
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

    def test_undo(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        stance = Stance(5)
        ship.stance = stance
        fit.ship = ship
        fit.purge_commands()
        fit.ship = None
        # Action
        fit.undo()
        # Pyfa model
        self.assertIs(ship.stance, stance)
        self.assertEqual(stance.eve_id, 5)
        self.assertEqual(stance.eve_name, 'Item 5 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.stance, fit.ship.stance._eos_item)
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
        self.assertEqual(fit.ship.stance.eve_id, 5)
        self.assertEqual(fit.ship.stance.eve_name, 'Item 5 (TQ)')
        # Eos model
        self.assertIs(fit._eos_fit.stance, fit.ship.stance._eos_item)

    def test_redo(self):
        fit = Fit(name='test fit 1')
        ship = Ship(1)
        stance = Stance(5)
        ship.stance = stance
        fit.ship = ship
        fit.purge_commands()
        fit.ship = None
        fit.undo()
        # Action
        fit.redo()
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
