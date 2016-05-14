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


class TestModelCharCoreGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_fit = self.eos_charcore_fit
        eos_fit.return_value = sentinel.efit
        sentinel.efit.character = sentinel.echar
        efit_calls_before = len(eos_fit.mock_calls)
        char = Character(alias='test char 1')
        efit_calls_after = len(eos_fit.mock_calls)
        # Pyfa model
        self.assertEqual(char.alias, 'test char 1')
        self.assertIs(char.source, self.source_tq)
        # Eos model
        self.assertEqual(efit_calls_after - efit_calls_before, 1)
        self.assertEqual(eos_fit.mock_calls[-1], call())
        self.assertIs(char._eos_fit, sentinel.efit)
        self.assertIs(char._eos_fit.source, self.eos_source_tq)
        self.assertIs(char._eos_item, sentinel.echar)

    def test_persistence(self):
        eos_fit = self.eos_charcore_fit
        eos_fit.return_value = sentinel.efit
        sentinel.efit.character = sentinel.echar
        char = Character(alias='test char 1')
        # Reload model via persistence (DB check)
        char.persist()
        efit_calls_before = len(eos_fit.mock_calls)
        self.pyfadb_force_reload()
        chars = self.query_chars()
        self.assertEqual(len(chars), 1)
        char = chars[0]
        efit_calls_after = len(eos_fit.mock_calls)
        # Pyfa model
        self.assertEqual(char.alias, 'test char 1')
        self.assertIs(char.source, self.source_tq)
        # Eos model
        self.assertEqual(efit_calls_after - efit_calls_before, 1)
        self.assertEqual(eos_fit.mock_calls[-1], call())
        self.assertIs(char._eos_fit, sentinel.efit)
        self.assertIs(char._eos_item, sentinel.echar)
