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


"""
There're two separate top-level entities in pyfa data model: fit and
character core.

- Character core carries 'metadata' about character - skills with their
levels, implants, API data and so on.
- Fit carries fit-specific data and objects. Character handling is somewhat
special for fit - when it gets some character assigned, character core
and all of its child objects are replicated to a fit into set of 'proxy'
objects. This is needed because we cannot store on character fit-specific
attributes (and on-character attributes are actively used by some modules).

Both of these objects have their own source management. That is, when fit
gets character core assigned, it doesn't matter if their sources match or
mismatch - fit uses only metadata from character core, ignoring source-
dependent content. Character proxies are using source of the fit.

Both of these entities have several models hidden beneath them. In this
module, we do all the magic to glue various models together:

  Pyfa model - how pyfa will use it, as in, our primary API for use by UI
  DB model - how it is stored in database
  Eos model - how Eos contains/manages fit

They are all different, thus logic might be complex at times. For example,
stance aka t3 tactical mode is stored on:

  Pyfa: fit.ship.stance
  DB: fit._stance_type_id
  Eos: efit.stance (efit is eos fit, which is stored on pyfa fit)

There's additional thing which needs to be processed, most pyfa items carry
reference to corresponding eve item (InvType), it also needs to be updated.

Thus, when we assign stance to ship, we should update reference to stance
on ship, and update DB/Eos stuff on fit level. The convention is to set
stance reference on ship within ship.stance setter, and handle DB/Eos/eve
item stuff in method which belongs to stance itself and is called from the
ship.stance setter. But there're also several other scenarios when one or
more models need to be updated, they have to be kept in mind when changing
anything:

  ship.stance is set when ship belongs to fit (scenario described above)
    Pyfa: update ship's stance reference
    DB: update fit._stance_type_id reference
    Eos: update efit.stance object
    EVE item: update

  ship.stance is set when ship doesn't belong to fit
    Pyfa: update ship's stance reference
    DB: no actions needed
    Eos: no actions needed
    EVE item: no actions needed (eve item exists only within scope of fit)

  ship with stance [assigned to/removed from] fit (ship stuff is omitted here)
    Pyfa: no actions needed
    DB: update fit._stance_type_id reference
    Eos: update efit.stance object
    EVE item: update

  fit source switch
    Pyfa: no actions needed
    DB: no actions needed
    Eos: no actions needed
    EVE item: update
"""

# Imports of modules which do not have dependencies on other Pyfa modules and
# which can be used from anywhere go first (to avoid import loops)
from .pyfadata_mgr import PyfaDataManager
from .base import PyfaBase
# Miscellanea imports - top-down from the most specific to most generic imports
# (because top-level objects sometimes import their children for reconstruction)
from .skill import Skill
from .subsystem import Subsystem
from .stance import Stance
from .character import Character
from .ship import Ship
from .fit import Fit


__all__ = [
    'Character',
    'Fit',
    'Ship',
    'Skill',
    'Stance',
    'Subsystem'
]



