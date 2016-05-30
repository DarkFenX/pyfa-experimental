import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'external')))

import os

from service.data.eve_data.query import *
from service.data.pyfa_data import *
from service.data.pyfa_data import PyfaDataManager
from service.source import SourceManager

eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
eve_dbpath_sisi = os.path.join(script_dir, 'staticdata', 'singularity.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize databases with eve data
SourceManager.add('tq', eve_dbpath_tq, make_default=True)
SourceManager.add('sisi', eve_dbpath_sisi)

# (Re-)Initialize database for pyfa save data
if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = PyfaDataManager.session


def print_attrs(item, orig=False):
    print('---{}---'.format(item.eve_name))
    if orig:
        attrs = item.attributes_original
    else:
        attrs = item.attributes
    for k in sorted(attrs, key=lambda i: i.name):
        print('  {}: {}'.format(k.name, attrs[k]))


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
DLP_LASER = 3001


def make_tengu():
    fit = Fit(name='test fit 1')
    fit.ship = Ship(TENGU)
    fit.ship.subsystems.add(Subsystem(TENGU_DEF_LINKS))
    fit.ship.subsystems.add(Subsystem(TENGU_ELE_ECCM))
    return fit


def make_confessor():
    fit = Fit(name='test fit 2')
    fit.ship = Ship(CONFESSOR, stance=Stance(CONFESSOR_DEFENSIVE_MODE))
    lasor = Module(DLP_LASER)
    fit.ship.modules.high.equip(lasor)
    print(fit.ship.modules)
    fit.persist()
    PyfaDataManager.commit()
    return fit

def make_character():
    char = Character(alias='Kadesh Priestess')
    for skill_type in query_published_skills(SourceManager.default.edb):
        char.skills.add(Skill(skill_type.id, level=5))
    return char


def test_random_shit():
    pass




def test_char_source_switch():
    warp_accu_tq = query_attribute(SourceManager.get('tq').edb, 1021)
    warp_accu_sisi = query_attribute(SourceManager.get('sisi').edb, 1021)
    char = Character(alias='test char 1')
    assert char.attributes[warp_accu_tq] == 15000
    assert char.attributes_original[warp_accu_tq] == 15000
    char.source = 'sisi'
    assert char.attributes[warp_accu_sisi] == 101
    assert char.attributes_original[warp_accu_sisi] == 202

make_confessor()
