import os

from data.pyfa_data import *
from data.pyfa_data import PyfaDataManager
from service import SourceManager

script_dir = os.path.dirname(os.path.abspath(__file__))
eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize database for tranquility
SourceManager.add_source('tq', eve_dbpath_tq)
session_evedata_tq = SourceManager.get_source('tq').edb

# (Re-)Initialize database for pyfa save data
if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = PyfaDataManager.session

CRUSADER = 11184
CHEETAH = 11182
CONFESSOR = 34317

fit = Fit('tq', name='test fit 1')
fit.ship = Ship(CONFESSOR)
print(fit.ship.eve_name)
print(fit.stats.agility_factor)
print(fit.ship.attributes)
print(fit.ship.effects)
session_pyfadata.add(fit)
session_pyfadata.commit()
fit.ship = Ship(CRUSADER)
print(fit.ship.eve_name)
print(fit.stats.agility_factor)
print(fit.ship.attributes)
print(fit.ship.effects)
session_pyfadata.add(fit)
session_pyfadata.commit()
