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


class TestModelSkillProxySourceSwitch(ModelTestCase):

    def test_do(self):
        char = Character(alias='test char 1')
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_core = Skill(6, level=3)
        char.skills.add(skill_core)
        # Action
        fit.source = self.source_sisi
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (SiSi)')
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
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        # We do not save fit's source into DB
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (TQ)')

    def test_undo(self):
        char = Character(alias='test char 1')
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_core = Skill(6, level=3)
        char.skills.add(skill_core)
        fit.source = self.source_sisi
        # Action
        fit.undo()
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (TQ)')
        # Command queue
        self.assertIs(fit.has_undo, False)
        self.assertIs(fit.has_redo, True)
        # We do not check persistence because source is not saved into DB

    def test_redo(self):
        char = Character(alias='test char 1')
        fit = Fit(name='test fit 1')
        fit.character_core = char
        skill_core = Skill(6, level=3)
        char.skills.add(skill_core)
        fit.source = self.source_sisi
        fit.undo()
        # Action
        fit.redo()
        # Pyfa model
        self.assertEqual(len(fit.character_proxy.skills), 1)
        skill_proxy = next(iter(fit.character_proxy.skills))
        self.assertEqual(skill_proxy.eve_id, 6)
        self.assertEqual(skill_proxy.eve_name, 'Item 6 (SiSi)')
        # Command queue
        self.assertIs(fit.has_undo, True)
        self.assertIs(fit.has_redo, False)
        # We do not check persistence because source is not saved into DB
