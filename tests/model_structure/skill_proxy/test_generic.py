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


class TestModelSkillProxyGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_skillproxy = self.eos_skillproxy
        eos_skillproxy.return_value = sentinel.eskill
        sentinel.eskill.level = 3
        char = Character(alias='test char 1')
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_core = Skill(6, level=3)
        eskill_calls_before = len(eos_skillproxy.mock_calls)
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        char.skills.add(skill_core)
        eskill_calls_after = len(eos_skillproxy.mock_calls)
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        self.assertEqual(skill_proxy.level, 3)
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (TQ)')
        # Eos model
        self.assertIs(skill_proxy._eos_item, sentinel.eskill)
        self.assertEqual(eskill_calls_after - eskill_calls_before, 1)
        self.assertEqual(eos_skillproxy.mock_calls[-1], call(6, level=3))
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.skills.mock_calls[-1], call.add(sentinel.eskill))
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, False)

    def test_persistence(self):
        eos_skillproxy = self.eos_skillproxy
        eos_skillproxy.return_value = sentinel.eskill
        sentinel.eskill.level = 3
        char = Character(alias='test char 1')
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_core = Skill(6, level=3)
        char.skills.add(skill_core)
        # Reload model via persistence (DB check)
        fit.persist()
        eskill_calls_before = len(eos_skillproxy.mock_calls)
        econt_calls_before = len(fit._eos_fit.skills.mock_calls)
        self.pyfadb_force_reload()
        fits = self.query_fits()
        self.assertEqual(len(fits), 1)
        fit = fits[0]
        eskill_calls_after = len(eos_skillproxy.mock_calls)
        econt_calls_after = len(fit._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        self.assertEqual(skill_proxy.level, 3)
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (TQ)')
        # Eos model
        self.assertIs(skill_proxy._eos_item, sentinel.eskill)
        self.assertEqual(eskill_calls_after - eskill_calls_before, 1)
        self.assertEqual(eos_skillproxy.mock_calls[-1], call(6, level=3))
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(fit._eos_fit.skills.mock_calls[-1], call.add(sentinel.eskill))
