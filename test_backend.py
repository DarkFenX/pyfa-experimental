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

def make_tengu():
    fit = Fit(name='test fit 1')
    fit.persist()
    fit.ship = Ship(TENGU)
    fit.ship.subsystems.add(Subsystem(TENGU_DEF_LINKS))
    fit.ship.subsystems.add(Subsystem(TENGU_ELE_ECCM))
    session_pyfadata.commit()

def make_confessor():
    fit = Fit(name='test fit 2')
    fit.ship = Ship(CONFESSOR)
    fit.ship.stance = Stance(CONFESSOR_DEFENSIVE_MODE)
    fit.persist()
    session_pyfadata.commit()

def test_chracters():
    char = Character(alias='Kadesh Priestess')
    #for skill_type in query_published_skills(SourceManager.default.edb):
    #    char.skills.add(Skill(skill_type.id, level=5))
    #char.persist()

def test_random_shit():
    fit = Fit(name='test fit 3')
    print(fit.source)
    print(fit._eos_fit.source)
    fit.ship = Ship(CONFESSOR)
    print(fit.ship)
    print(fit.ship.eve_id)
    print(fit.ship.eve_name)
    print(fit.ship.attributes)
    print(fit.ship.attributes_original)

#make_tengu()
#make_confessor()
test_random_shit()
