import os

from data.pyfa_data import *
import config


script_dir = os.path.dirname(os.path.abspath(__file__))
eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize database for tranquility
config.eve_sources.add_source('tq', eve_dbpath_tq)
session_evedata_tq = config.eve_sources['tq'].edb

# (Re-)Initialize database for pyfa save data
if os.path.isfile(pyfa_dbpath): os.remove(pyfa_dbpath)
config.set_pyfadb_path(pyfa_dbpath)
session_pyfadata = config.pyfadb_session

fit = Fit('tq', name='test fit 1')
fit.ship = Ship(11182)
print(fit.ship._eve_item)
session_pyfadata.add(fit)
session_pyfadata.commit()
