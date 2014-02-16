import py
import sqlite3
from functools import wraps
from contextlib import closing

IMPORT = "insert or ignore into filename_blob (blob, name) values (?, ?)"
REPOS = '''
    select distinct substr(name, 0, instr(name, :type))
    from fts_filename
    where name match :type
    order by name
'''


def do_migrate(dbname):
    from micromigrate import find_in_path, apply_migrations
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))
    print migrations
    from micromigrate.backend_script import ScriptBackend
    migrator = ScriptBackend(dbname)
    apply_migrations(migrator, migrations)


def appcommand(func):
    @wraps(func)
    def command(dbname, *args):
        do_migrate(dbname)
        db = sqlite3.connect(dbname)
        with closing(db):
            func(db, *args)
    return command

@appcommand
def repos(db, type_):
    results = db.execute(REPOS, {'type': '.' + type_})
    for item in results:
        print(item[0])

@appcommand
def load(db, filename):
    with open(filename) as fp:
        items = [line.decode('utf-8', 'replace').split('  ', 1) for line in fp]
    db.executemany(IMPORT, items)
    db.commit()





