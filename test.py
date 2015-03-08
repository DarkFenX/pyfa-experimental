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

SourceManager.add_source('sisi', eve_dbpath_tq)

# (Re-)Initialize database for pyfa save data
if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = PyfaDataManager.session

CRUSADER = 11184
CHEETAH = 11182
CONFESSOR = 34317
CONFESSOR_DEFENSIVE_MODE = 34319

fit = Fit('tq', name='test fit 1')
#fit.ship = Ship(CONFESSOR)
#print(dict((k.name, v)for k, v in fit.ship.attributes.items())['armorEmDamageResonance'])
#fit.ship.stance = Stance(CONFESSOR_DEFENSIVE_MODE)
#print(dict((k.name, v)for k, v in fit.ship.attributes.items())['armorEmDamageResonance'])
conf = Ship(CONFESSOR, stance=Stance(CONFESSOR_DEFENSIVE_MODE))
fit.ship = conf
print(dict((k.name, v)for k, v in fit.ship.attributes.items())['armorEmDamageResonance'])


session_pyfadata.add(fit)
session_pyfadata.commit()
