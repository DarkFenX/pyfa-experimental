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


from sqlalchemy.orm.util import has_identity

from .pyfadata_mgr import PyfaDataManager


def get_src_children(child_list):
    """
    Accept iterable of source-dependent child objects (some
    of which may be None) and compose set, which includes all
    passed child objects and their source-dependent children too.
    """
    children = set()
    for child in child_list:
        if child is None:
            continue
        children.add(child)
        if hasattr(child, '_src_children'):
            children.update(child._src_children)
    return children


# Object persistence functions for pyfa database session
def pyfa_persist(obj):
    """
    Add object to pyfa data session to make sure it's saved on commit.
    """
    PyfaDataManager.session.add(obj)


def pyfa_abandon(obj):
    """
    Remove object from database session.
    """
    db_session = PyfaDataManager.session
    # If object isn't in session (transient or detached state),
    # do not do anything at all
    if db_session is None:
        return
    # Delete if persistent state
    if has_identity(obj):
        db_session.delete(obj)
    # Expunge if pending state
    else:
        db_session.expunge(obj)
