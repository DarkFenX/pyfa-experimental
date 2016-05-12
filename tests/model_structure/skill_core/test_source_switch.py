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


class TestModelSkillCoreSourceSwitch(ModelTestCase):

    def test_do(self):
        char = Character(alias='test char 1')
        skill = Skill(3, level=2)
        char.skills.add(skill)
        # Action
        char.source = self.source_sisi
        # Pyfa model
        self.assertEqual(skill.eve_id, 3)
        self.assertEqual(skill.level, 2)
        self.assertEqual(skill.eve_name, 'Item 3 (SiSi)')
        # Reload model via persistence (DB check)
        char.persist()
        self.pyfadb_force_reload()
        chars = self.query_chars()
        self.assertEqual(len(chars), 1)
        char = chars[0]
        # Pyfa model
        self.assertEqual(len(char.skills), 1)
        skill = next(iter(char.skills))
        self.assertEqual(skill.eve_id, 3)
        self.assertEqual(skill.level, 2)
        # We do not save fit's source into DB
        self.assertEqual(skill.eve_name, 'Item 3 (TQ)')
