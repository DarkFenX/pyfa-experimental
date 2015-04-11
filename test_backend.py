import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'external')))

import os

from service.data.eve_data.query import *
from service.data.pyfa_data import *
from service.data.pyfa_data import PyfaDataManager
from service.source_mgr import SourceManager

eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize databases with eve data
SourceManager.add('tq', eve_dbpath_tq, make_default=True)
SourceManager.add('sisi', eve_dbpath_tq)

# (Re-)Initialize database for pyfa save data
if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = PyfaDataManager.session

CRUSADER = 11184
CHEETAH = 11182
CONFESSOR = 34317
CONFESSOR_DEFENSIVE_MODE = 34319
CONFESSOR_SNIPER_MODE = 34321
TENGU = 29984
TENGU_DEF_LINKS = 29972
TENGU_DEF_EHP = 29971
TENGU_OFF_MISSILES = 30122
TENGU_ENG_CAPREGEN = 30143
TENGU_PROP_WARP = 30088
TENGU_ELE_ECCM = 30050

fit1 = Fit(name='test fit 1')
fit1.persist()
fit1.ship = Ship(TENGU)
for k in sorted(fit1.ship._eve_item.attributes, key=lambda a: a.name):
    print(k.name, fit1.ship._eve_item.attributes[k])
print('---')
for i in sorted(fit1.ship._eve_item.effects, key=lambda i: i.name):
    print(i.name)
print('---')
print(fit1.ship._eve_item._dgmtypeeffects)
#fit1.ship.subsystems.add(Subsystem(TENGU_DEF_LINKS))
#fit1.ship.subsystems.add(Subsystem(TENGU_ELE_ECCM))
#session_pyfadata.commit()

#fit2 = Fit(name='test fit 2')
#fit2.ship = Ship(CONFESSOR)
#fit2.ship.stance = Stance(CONFESSOR_DEFENSIVE_MODE)
#fit2.persist()
#session_pyfadata.commit()

#char = Character(alias='Kadesh Priestess')
#for skill_type in get_published_skills(SourceManager.default.edb):
#    char.skills.add(Skill(skill_type.id, level=5))
#char.persist()

#session_pyfadata.commit()
