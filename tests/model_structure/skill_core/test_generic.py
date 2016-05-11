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


class TestModelSkillCoreGeneric(ModelTestCase):

    def test_instantiation(self):
        eos_skillcore = self.eos_skillcore
        eos_skillcore.return_value = sentinel.eskill
        char = Character(alias='test char 1')
        eskill_calls_before = len(eos_skillcore.mock_calls)
        econt_calls_before = len(char._eos_fit.skills.mock_calls)
        skill = Skill(6, level=3)
        eskill_calls_after = len(eos_skillcore.mock_calls)
        econt_calls_after = len(char._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(skill.eve_id, 6)
        self.assertEqual(skill.level, 3)
        self.assertIs(skill.eve_name, None)
        # Eos model
        self.assertEqual(eskill_calls_after - eskill_calls_before, 1)
        self.assertEqual(eos_skillcore.mock_calls[-1], call(6, level=3))
        self.assertEqual(econt_calls_after - econt_calls_before, 0)
        self.assertIs(skill._eos_item, sentinel.eskill)

    def test_persistence(self):
        eos_skillcore = self.eos_skillcore
        eos_skillcore.return_value = sentinel.eskill
        char = Character(alias='test char 1')
        skill = Skill(6, level=3)
        char.skills.add(skill)
        # Reload model via persistence (DB check)
        char.persist()
        eskill_calls_before = len(eos_skillcore.mock_calls)
        econt_calls_before = len(char._eos_fit.skills.mock_calls)
        self.pyfadb_force_reload()
        chars = self.query_chars()
        self.assertEqual(len(chars), 1)
        char = chars[0]
        eskill_calls_after = len(eos_skillcore.mock_calls)
        econt_calls_after = len(char._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(char.skills), 1)
        skill = next(iter(char.skills))
        self.assertEqual(skill.eve_id, 6)
        self.assertEqual(skill.level, 3)
        self.assertEqual(skill.eve_name, 'Item 6 (TQ)')
        # Eos model
        self.assertEqual(eskill_calls_after - eskill_calls_before, 1)
        self.assertEqual(eos_skillcore.mock_calls[-1], call(6, level=3))
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(char._eos_fit.skills.mock_calls[-1], call.add(sentinel.eskill))
