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

from eos import SourceManager as EosSourceManager, SQLiteDataHandler, JsonCacheHandler
from util.repr import make_repr_str
from .data.eve_data import make_evedata_session
from .exception import ExistingSourceError, UnknownSourceError


Source = namedtuple('Source', ('alias', 'edb', 'eos'))


class SourceManager:
    """
    Handle and access different sources in an easy way. Useful for cases
    when you want to work with, for example, Tranquility and Singularity
    data at the same time.
    """

    # Format:
    # {literal alias: Source}
    _sources = {}

    # Default source, will be used implicitly in many cases
    # when service user doesn't set it explicitly
    default = None

    @classmethod
    def add(cls, alias, db_path, make_default=False):
        """
        Add source to source manager - this includes initializing
        all facilities hidden behind name 'source'. After source
        has been added, it is accessible with alias.

        Required arguments:
        alias -- alias under which source will be accessible. Also
        controls several paths under which temporary data is stored
        for the sources
        db_path -- path to database with EVE data for this source

        Optional arguments:
        make_default -- marks passed source default; it will be used
        by default for some actions, like fit initialization, unless
        specified explicitly
        """
        if alias in cls._sources:
            raise ExistingSourceError(alias)
        # Database session
        edb_session = make_evedata_session(db_path)
        # Eos source
        data_handler = SQLiteDataHandler(db_path)
        cache_handler = JsonCacheHandler('staticdata/eos_cache/{}.json.bz2'.format(alias))
        EosSourceManager.add(alias, data_handler, cache_handler)
        eos_source = EosSourceManager.get(alias)
        # Finally, add record to list of sources
        source = Source(alias=alias, edb=edb_session, eos=eos_source)
        cls._sources[alias] = source
        if make_default is True:
            cls.default = source

    @classmethod
    def get(cls, alias):
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
        except KeyError:
            raise UnknownSourceError(alias)

    @classmethod
    def remove(cls, alias):
        """
        Remove source by alias.

        Required arguments:
        alias -- alias of source to remove
        """
        try:
            source = cls._sources[alias]
        except KeyError:
            raise UnknownSourceError(alias)
        else:
            EosSourceManager.remove(alias)
            source.edb_session.close()

    @classmethod
    def list(cls):
        return list(cls._sources.keys())

    @classmethod
    def __repr__(cls):
        spec = [['sources', '_sources']]
        return make_repr_str(cls, spec)
