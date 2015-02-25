#===============================================================================
# Copyright (C) 2015 Anton Vorobyov
#
# This file is part of Pyfa 3.
#
# Pyfa 3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyfa 3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyfa 3. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from collections import namedtuple

from data.eve_data import make_evedata_session
from eos import Eos, SQLiteDataHandler, JsonCacheHandler, TextLogger


Source = namedtuple('Source', ('edb_session', 'eos_instance'))


class SourceManager:

    _instance = None

    def __init__(self):
        # Format:
        # {literal alias: Source(eve data database session, eos instance)}
        self._sources = {}

    @classmethod
    def getinst(cls):
        if cls._instance is None:
            cls._instance = SourceManager()
        return cls._instance

    def add_source(self, alias, db_path):
        # Database session
        edb_session = make_evedata_session(db_path)
        logger = TextLogger('eos_{}'.format(alias), 'userdata/eos_logs/{}.log'.format(alias))
        data_handler = SQLiteDataHandler(db_path)
        cache_handler = JsonCacheHandler('staticdata/eos_cache/{}.json.bz2'.format(alias), logger)
        eos_instance = Eos(data_handler, cache_handler, logger)
        self._sources[alias] = Source(edb_session, eos_instance)

    def __getitem__(self, src_alias):
        return self._sources[src_alias]
