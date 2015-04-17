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


import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .base import EveBase
from .dgmattribute import DgmAttribute
from .dgmeffect import DgmEffect
from .dgmexpression import DgmExpression
from .invgroup import InvGroup
from .invmarketgroup import InvMarketGroup
from .invtype import InvType
from .phbmetadata import PhbMetaData
# Just for initialization
from .dgmtypeattribute import DgmTypeAttribute
from .dgmtypeeffect import DgmTypeEffect


__all__ = [
    'DgmAttribute',
    'DgmEffect',
    'DgmExpression',
    'InvGroup',
    'InvMarketGroup',
    'InvType',
    'PhbMetaData'
]


def make_evedata_session(db_path):
    evedb_engine = sqlalchemy.create_engine('sqlite:///{}'.format(db_path), echo=False)
    EveBase.metadata.create_all(evedb_engine)
    evedb_session = sessionmaker(bind=evedb_engine)()
    return evedb_session
