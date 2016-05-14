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


class TestModelCharProxySyncCharCore(ModelTestCase):

    def test_add(self):
        fit = Fit(name='test fit 1')
        char_core = Character(alias='test char 1')
        # Action
        fit.character_core = char_core
        # Pyfa model
        self.assertEqual(fit.character_proxy.alias, 'test char 1')
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.character_proxy.alias, 'test char 1')
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')

    def test_remove(self):
        fit = Fit(name='test fit 1')
        char_core = Character(alias='test char 1')
        fit.character_core = char_core
        # Action
        fit.character_core = None
        # Pyfa model
        self.assertIs(fit.character_proxy.alias, None)
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertIs(fit.character_proxy.alias, None)
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')


    def test_change(self):
        fit = Fit(name='test fit 1')
        char_core1 = Character(alias='test char 1')
        char_core2 = Character(alias='test char 2')
        fit.character_core = char_core1
        # Action
        fit.character_core = char_core2
        # Pyfa model
        self.assertEqual(fit.character_proxy.alias, 'test char 2')
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)
        # Reload model via persistence (DB check)
        fit.persist()
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        # Pyfa model
        self.assertEqual(fit.character_proxy.alias, 'test char 2')
        self.assertEqual(fit.character_proxy.eve_id, 1381)
        self.assertEqual(fit.character_proxy.eve_name, 'Item 1381 (TQ)')
