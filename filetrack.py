import sys
import py
import sqlite3

IMPORT= "insert or ignore into filename_blob (blob, name) values (?, ?)"

def do_migrate(dbname):
    from micromigrate import find_in_path, apply_migrations
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))
    print migrations
    from micromigrate.backend_script import ScriptBackend
    migrator = ScriptBackend(dbname)
    apply_migrations(migrator, migrations)


def load(dbname, filename):
    do_migrate(dbname)
    with open(filename) as fp:
       items = [line.decode('utf-8', 'replace').split('  ', 1) for line in fp]
    db = sqlite3.connect(dbname);
    db.executemany(IMPORT, items)
    db.commit()
    db.close()



if __name__ == '__main__':
    args = sys.argv[2:]
    command = sys.argv[1]
    globals()[command](*args)

