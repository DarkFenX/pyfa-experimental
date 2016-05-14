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


class TestModelCharProxyGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_charproxy = self.eos_charproxy
        eos_charproxy.return_value = sentinel.echar
        echar_calls_before = len(eos_charproxy.mock_calls)
        fit = Fit(name='test fit 1')
        echar_calls_after = len(eos_charproxy.mock_calls)
        # Pyfa model
        self.assertIs(fit.character_proxy.alias, None)
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')
        # Eos model
        self.assertEqual(echar_calls_after - echar_calls_before, 1)
        self.assertEqual(eos_charproxy.mock_calls[-1], call(1381))
        # Character proxy is assigned to fit by default, even when there's
        # no character core assigned
        self.assertIs(fit._eos_fit.character, sentinel.echar)
        self.assertIs(fit._eos_fit.character, fit.character_proxy._eos_item)
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
