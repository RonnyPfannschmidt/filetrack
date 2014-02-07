import sys
import py
import sqlite3

IMPORT= "insert or ignore into filename_blob (filename, checksum) values (?, ?)"

def do_migrate(dbname):
    from micromigrate import find_in_path, apply_ migrations
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = find_in_path(here)
    migrator = ScriptBackend(dbname)
    apply_migrations(migrator, migrations)



def import(dbname, filename):
    do_migrate(dbname)
    with open(f) as fp:
       items = [line.split('  ', 1) for line in fp]
    db = sqlite3.connect(dbname);
    db.executemany(IMPORT, items)


if 
