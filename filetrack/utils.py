import py
import sqlite3
from contextlib import closing
from functools import wraps

from micromigrate import find_in_path, apply_migrations, missing_migrations
from micromigrate.backend_script import ScriptBackend


def needs_migrate(dbname):
    return _micromigrate(dbname, missing_migrations)

def do_migrate(dbname):
    _micromigrate(sbname, apply_migrations)

def _micromigrate(dbname, command):
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))
    migrator = ScriptBackend(dbname)
    return command(migrator, migrations)


def appcommand(func):
    @wraps(func)
    def command(dbname, *args):
        missing = needs_migrate(dbname)
        if missing:
            print 'missing migrations', sorted(missing)
            raise SystemExit(1)
        db = sqlite3.connect(dbname)
        with closing(db):
            func(db, *args)
    return command
