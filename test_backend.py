import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'dependency')))

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
print(fit.stats.hp)
sub_links = Subsystem(TENGU_DEF_LINKS)
sub_ehp = Subsystem(TENGU_DEF_EHP)
fit.ship.subsystems.add(sub_links)
print(fit.stats.hp)
session_pyfadata.add(fit)
session_pyfadata.commit()
fit.ship.subsystems.remove(sub_links)
fit.ship.subsystems.add(sub_ehp)
print(fit.stats.hp)
session_pyfadata.commit()
fit.undo()
print(fit.stats.hp)
print(fit.stats.cpu.output)
fit.ship.subsystems.add(Subsystem(TENGU_ELE_ECCM))
print(fit.stats.cpu.output)
fit.ship.subsystems.add(Subsystem(TENGU_OFF_MISSILES))
print(fit.stats.cpu.output)
#session_pyfadata.commit()
fit.ship.subsystems.clear()
print(fit.stats.cpu.output)
fit.undo()
print(fit.stats.cpu.output)
session_pyfadata.commit()
