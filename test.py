import os

from data.eve_data import *
from data.pyfa_data import *
import config


script_dir = os.path.dirname(os.path.abspath(__file__))
eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'pyfadata.db')


# Initialize database for tranquility
config.eve_sources.add_source('tq', eve_dbpath_tq)
session_evedata_tq = config.eve_sources['tq'].edb_session

# (Re-)Initialize database for pyfa save data
os.remove(pyfa_dbpath)
config.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = config.pyfadb_session

for i in session_evedata_tq.query(InvType):
    print('---')
    print(i.type_name)
    print(i.attributes)
    print(i.effects)

#fit = Fit('tq', name='testfit')
#fit.ship = Ship(132)
#fit = DFit(name='test fit')
#mod1 = DModule(type_id=55, rack=0, position=2)
#mod2 = DModule(type_id=66, rack=0, position=3)
#mod3 = DModule(type_id=77, rack=2, position=0)

#fit._modules.append(mod1)
#fit._modules.append(mod2)
#fit._modules.append(mod3)
#session_pyfadata.add(fit)
#session_pyfadata.commit()
#print(fit.modules_high)
