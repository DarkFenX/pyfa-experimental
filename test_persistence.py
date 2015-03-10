import os.path
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, 'external')))

import os

from service.data.eve_data import *
from service.data.pyfa_data import *
from service.data.pyfa_data import PyfaDataManager
from service.data.pyfa_data.query import *
from service.source_mgr import SourceManager

eve_dbpath_tq = os.path.join(script_dir, 'staticdata', 'tranquility.db')
pyfa_dbpath = os.path.join(script_dir, 'userdata', 'pyfadata.db')

# Initialize database for tranquility
SourceManager.add_source('tq', eve_dbpath_tq)
session_evedata_tq = SourceManager.get_source('tq').edb

SourceManager.add_source('sisi', eve_dbpath_tq)

# Initialize database for pyfa save data
PyfaDataManager.set_pyfadb_path(pyfa_dbpath)

for fit in get_all_fits():
    print(fit)
