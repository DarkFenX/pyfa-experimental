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


from unittest.mock import call, sentinel

from service.data.pyfa_data import *
from tests.model_structure.model_testcase import ModelTestCase


class TestModelSubsystemGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_subsystem = self.eos_subsystem
        eos_subsystem.return_value = sentinel.esubsystem
        fit = Fit(name='test fit 1', ship=Ship(1))
        esubsystem_calls_before = len(eos_subsystem.mock_calls)
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        subsystem = Subsystem(9)
        esubsystem_calls_after = len(eos_subsystem.mock_calls)
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(subsystem.eve_id, 9)
        self.assertIs(subsystem.eve_name, None)
        # Eos model
        self.assertEqual(esubsystem_calls_after - esubsystem_calls_before, 1)
        self.assertEqual(eos_subsystem.mock_calls[-1], call(9))
        self.assertEqual(econt_calls_after - econt_calls_before, 0)
        self.assertIs(subsystem._eos_item, sentinel.esubsystem)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)

    def test_persistence(self):
        eos_subsystem = self.eos_subsystem
        eos_subsystem.return_value = sentinel.esubsystem
        fit = Fit(name='test fit 1', ship=Ship(1))
        fit.ship.subsystems.add(Subsystem(9))
        # Reload model via persistence (DB check)
        fit.persist()
        esubsystem_calls_before = len(eos_subsystem.mock_calls)
        econt_calls_before = len(fit._eos_fit.subsystems.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        esubsystem_calls_after = len(eos_subsystem.mock_calls)
        econt_calls_after = len(fit._eos_fit.subsystems.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.ship.subsystems), 1)
        subsystem = next(iter(fit.ship.subsystems))
        self.assertEqual(subsystem.eve_id, 9)
        self.assertEqual(subsystem.eve_name, 'Item 9 (TQ)')
        # Eos model
        self.assertEqual(esubsystem_calls_after - esubsystem_calls_before, 1)
        self.assertEqual(eos_subsystem.mock_calls[-1], call(9))
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.subsystems.mock_calls[-1], call.add(sentinel.esubsystem))
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
