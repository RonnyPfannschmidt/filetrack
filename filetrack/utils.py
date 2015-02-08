from __future__ import print_function
import py
import sqlite3
import json
from os import path
from contextlib import closing, contextmanager
from functools import wraps

from micromigrate import find_in_path, apply_migrations, missing_migrations
from micromigrate.backend_script import ScriptBackend


def needs_migrate(dbname):
    return _micromigrate(dbname, missing_migrations)


def do_migrate(dbname):
    _micromigrate(dbname, apply_migrations)


def _micromigrate(dbname, command):
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))
    migrator = ScriptBackend(dbname)
    return command(migrator, migrations)


class CollectList(object):
    def __init__(self):
        self.data = []

    def step(self, value):
        self.data.append(value)

    def finalize(self):
        return json.dumps(self.data)


@contextmanager
def database(dbname):
    conn = sqlite3.connect(dbname)

    def my_basename(arg):
        arg = path.basename(arg)
        arg = arg.strip()
        if arg.endswith('.i'):
            arg = arg[:-2]
        return arg

    conn.create_function('basename', 1, my_basename)
    conn.create_aggregate('collect_list', 1, CollectList)
    with closing(conn):
        yield conn


def appcommand(func):
    @wraps(func)
    def command(dbname, *args):
        missing = needs_migrate(dbname)
        if missing:
            print('missing migrations', sorted(missing))
            raise SystemExit(1)
        with database(dbname) as db:
            func(db, *args)
    return command


_notify = print


def simplerows(db, query, args):
    print(args)
    if args is not None:
        rows = db.execute(query, args)
    else:
        rows = db.execute(query)
    for row in rows:
        _notify(*row)
