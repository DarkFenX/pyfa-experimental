#!/usr/bin/env python3
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


import argparse
import os.path
import sys
import unittest


script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Pyfa paths to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', 'external')))


if __name__ == '__main__':

    if sys.version_info.major != 3 or sys.version_info.minor < 3:
        sys.stderr.write('Tests require at least python 3.3 to run\n')
        sys.exit()

    # Parse command line option (which is optional and positional)
    parser = argparse.ArgumentParser(description='Run Pyfa tests')
    parser.add_argument(
        'suite', nargs='?', type=str,
        help='system or module path to test suite to run, defaults to all tests',
        default=script_dir
    )
    args = parser.parse_args()
    # Get all tests into suite
    tests = unittest.TestLoader().discover(args.suite, 'test_*.py')
    # Run them
    unittest.TextTestRunner().run(tests)
