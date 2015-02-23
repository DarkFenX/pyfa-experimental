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


import os
import sys


# Add Pyfa folder to import paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))


import argparse
import json

import sqlalchemy

import data.eve_data


# Format:
# {JSON file name: (SQLAlchemy entity, {source field name: target column name})}
tables = {
    'dgmattribs': (
        data.eve_data.DgmAttribute,
        {}
    ),
    'dgmeffects': (
        data.eve_data.DgmEffect,
        {}
    ),
    'dgmtypeattribs': (
        data.eve_data.DgmTypeAttribute,
        {}
    ),
    'dgmtypeeffects': (
        data.eve_data.DgmTypeEffect,
        {}
    ),
    'invtypes': (
        data.eve_data.InvType,
        {'typeName_en-us': 'clsname'}
    )
}


def process_table(edb_session, json_path, json_name):
    """
    Handle flow of how JSON is converted into table.
    """
    print('processing {}'.format(json_name))
    table_data = load_table(json_path, json_name)
    write_table(edb_session, json_name, table_data)


def load_table(json_path, json_name):
    """
    Load JSON file related to specified table and return it.
    """
    with open(os.path.join(json_path, '{}.json'.format(json_name))) as f:
        return json.load(f)

def write_table(edb_session, json_name, table_data):
    """
    Generate objects using passed data and add them to database session.
    """
    cls, replacements = tables[json_name]
    # Compose map which will help us to handle differences between SQL Alchemy
    # attribute names and actual SQL column names. Format:
    # {column name: attribute name to access it}
    alche_map = {}
    for attr in sqlalchemy.inspect(cls).attrs:
        # We're not interested in anything but column descriptors
        if not isinstance(attr, sqlalchemy.orm.ColumnProperty):
            continue
        for column in attr.columns:
            alche_map[column.name] = attr.key
    for row in table_data:
        instance = cls()
        for src_field_name, value in row.items():
            tgt_column_name = replacements.get(src_field_name, src_field_name)
            tgt_attr_name = alche_map.get(tgt_column_name, tgt_column_name)
            setattr(instance, tgt_attr_name, value)
        edb_session.add(instance)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This script converts Phobos JSON dump into database usable by pyfa.')
    parser.add_argument('-j', '--json', required=True, type=str, help='The path to Phobos json dump')
    parser.add_argument('-d', '--db', required=True, type=str, help='Path to database')
    args = parser.parse_args()

    # Expand home folder if needed
    json_path = os.path.expanduser(args.json)
    db_path = os.path.expanduser(args.db)

    # Check if there's a file at DB path, and if it's there, remove it
    if os.path.isfile(db_path):
        os.remove(db_path)

    edb_session = data.eve_data.make_evedata_session(db_path)

    for json_name in sorted(tables):
        process_table(edb_session, json_path, json_name)

    print('committing')
    edb_session.commit()
