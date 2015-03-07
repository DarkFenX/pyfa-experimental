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


class PyfaError(Exception):
    """
    All pyfa exceptions are based on this class.
    """
    pass


# Source manager exceptions
class UnknownSourceError(PyfaError):
    """
    Raised when source corresponding to passed alias
    cannot be found.
    """
    pass


# Command manager exceptions
class EmptyCommandQueueError(PyfaError):
    """
    Raised on attempt to undo or redo command when
    corresponding queue is empty.
    """
    pass


class ExecutedFlagError(PyfaError):
    """
    Raised when already executed command is ran or
    not executed command is undone.
    """
    pass
