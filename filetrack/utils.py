from micromigrate import find_in_path, apply_migrations
from micromigrate.backend_script import ScriptBackend


def do_migrate(dbname):
    here = py.path.local(__file__).dirpath().join('migrations')
    migrations = list(find_in_path(here))
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
