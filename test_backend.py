import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'external')))

import os

from service.data.eve_data import *
from service.data.pyfa_data import *
from service.data.pyfa_data import PyfaDataManager
from service.source_mgr import SourceManager

eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize database for tranquility
SourceManager.add_source('tq', eve_dbpath_tq)
session_evedata_tq = SourceManager.get_source('tq').edb

SourceManager.add_source('sisi', eve_dbpath_tq)

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

fit = Fit('tq', name='test fit 1')
fit.ship = Ship(TENGU)
sub_def_links = Subsystem(TENGU_DEF_LINKS)
sub_def_ehp = Subsystem(TENGU_DEF_EHP)
sub_ele_eccm = Subsystem(TENGU_ELE_ECCM)
fit.ship.subsystems.add(sub_def_links)
fit.ship.subsystems.add(sub_ele_eccm)
fit.persist()
session_pyfadata.commit()
fit.ship.subsystems.remove(sub_def_links)
session_pyfadata.commit()
#fit.abandon()
#session_pyfadata.commit()
