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


class TestModelSkillCoreAttachedRemove(ModelTestCase):

    def test_do(self):
        char = Character(alias='test char 1')
        skill = Skill(9, level=5)
        char.skills.add(skill)
        # Action
        econt_calls_before = len(char._eos_fit.skills.mock_calls)
        char.skills.remove(skill)
        econt_calls_after = len(char._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(char.skills), 0)
        self.assertEqual(skill.eve_id, 9)
        self.assertEqual(skill.level, 5)
        self.assertIs(skill.eve_name, None)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 1)
        self.assertEqual(char._eos_fit.skills.mock_calls[-1], call.remove(skill._eos_item))
        # Reload model via persistence (DB check)
        char.persist()
        econt_calls_before = len(char._eos_fit.skills.mock_calls)
        self.pyfadb_force_reload()
        chars = self.query_chars()
        self.assertEqual(len(chars), 1)
        char = chars[0]
        econt_calls_after = len(char._eos_fit.skills.mock_calls)
        # Pyfa model
        self.assertEqual(len(char.skills), 0)
        # Eos model
        self.assertEqual(econt_calls_after - econt_calls_before, 0)
