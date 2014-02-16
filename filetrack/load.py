from .utils import appcommand

IMPORT = "insert or ignore into filename_blob (blob, name) values (?, ?)"


@appcommand
def load(db, filename):
    with open(filename) as fp:
        items = [line.decode('utf-8', 'replace').split('  ', 1) for line in fp]
    db.executemany(IMPORT, items)
    db.commit()
