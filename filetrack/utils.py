from __future__ import print_function
import py
import json
from os import path
import sqlite3
import click
from micromigrate import find_in_path, apply_migrations, missing_migrations
from micromigrate.backend_script import ScriptBackend


def connect(dbname, auto_migrate):
    backend = ScriptBackend(dbname)
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))

    if auto_migrate:
        apply_migrations(backend, migrations)
    else:
        missing = missing_migrations(backend, migrations)
        if missing:
            click.echo('missing migrations %s' % (
                ', '.join(missing)))
            raise click.Abort()

    conn = sqlite3.connect(dbname)
    conn.create_function('basename', 1, my_basename)
    conn.create_aggregate('listagg', 1, CollectList)
    return conn


class CollectList(object):
    def __init__(self):
        self.data = []

    def step(self, value):
        self.data.append(value)

    def finalize(self):
        return json.dumps(self.data)


def my_basename(arg):
    arg = path.basename(arg)
    arg = arg.strip()
    if arg.endswith('.i'):
        arg = arg[:-2]
    return arg

_notify = print


def simplerows(db, query, args=()):
    if args:
        print(args)
    rows = db.execute(query)
    for row in rows:
        _notify(*row)
