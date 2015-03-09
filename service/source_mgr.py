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

from eos import Eos, SQLiteDataHandler, JsonCacheHandler, TextLogger
from .data.eve_data import make_evedata_session
from .exception import UnknownSourceError


Source = namedtuple('Source', ('alias', 'edb', 'eos'))


class SourceManager:
    """
    Handle and access different sources in an easy way. Useful for cases
    when you want to work with, for example, Tranquility and Singularity
    data at the same time.
    """

    # Format:
    # {literal alias: Source(eve data database session, eos instance)}
    _sources = {}

    @classmethod
    def add_source(cls, alias, db_path):
        """
        Add source to source manager - this includes initializing
        all facilities hidden behind name 'source'. After source
        has been added, it is accessible with alias.

        Required arguments:
        alias -- alias under which source will be accessible. Also
        controls several paths under which temporary data is stored
        for the sources
        db_path -- path to database with EVE data for this source
        """
        # Database session
        edb_session = make_evedata_session(db_path)
        # Eos instance
        logger = TextLogger('eos_{}'.format(alias), 'userdata/eos_logs/{}.log'.format(alias))
        data_handler = SQLiteDataHandler(db_path)
        cache_handler = JsonCacheHandler('staticdata/eos_cache/{}.json.bz2'.format(alias), logger)
        eos_instance = Eos(data_handler, cache_handler, logger)
        # Finally, add record to list of sources
        cls._sources[alias] = Source(alias=alias, edb=edb_session, eos=eos_instance)

    @classmethod
    def get_source(cls, alias):
        """
        Using source alias, return source data.

        Required arguments:
        alias -- alias of source to return

        Return value:
        (alias, edb, eos) named tuple with alias,
        SQL Alchemy database session and Eos instance for requested
        source
        """
        try:
            return cls._sources[alias]
        except KeyError as e:
            raise UnknownSourceError
