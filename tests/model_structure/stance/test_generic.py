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


class TestModelStanceGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_stance = self.eos_stance
        eos_stance.return_value = sentinel.estance
        fit = Fit(name='test fit 1', ship=Ship(1))
        estance_calls_before = len(eos_stance.mock_calls)
        stance = Stance(4)
        estance_calls_after = len(eos_stance.mock_calls)
        # Pyfa model
        self.assertEqual(stance.eve_id, 4)
        self.assertIs(stance.eve_name, None)
        # Eos model
        self.assertEqual(estance_calls_after - estance_calls_before, 1)
        self.assertEqual(eos_stance.mock_calls[-1], call(4))
        self.assertIs(fit._eos_fit.stance, None)
        self.assertIs(stance._eos_item, sentinel.estance)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)

    def test_persistence(self):
        eos_stance = self.eos_stance
        eos_stance.return_value = sentinel.estance
        fit = Fit(name='test fit 1', ship=Ship(1))
        fit.ship.stance = Stance(4)
        # Reload model via persistence (DB check)
        fit.persist()
        estance_calls_before = len(eos_stance.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        estance_calls_after = len(eos_stance.mock_calls)
        # Pyfa model
        self.assertEqual(fit.ship.stance.eve_id, 4)
        self.assertEqual(fit.ship.stance.eve_name, 'Item 4 (TQ)')
        # Eos model
        self.assertEqual(estance_calls_after - estance_calls_before, 1)
        self.assertEqual(eos_stance.mock_calls[-1], call(4))
        self.assertIs(fit._eos_fit.stance, sentinel.estance)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
