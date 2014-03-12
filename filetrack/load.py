import hashlib
import functools
from .utils import appcommand

IMPORT = "insert or ignore into filename_blob (blob, name) values (?, ?)"
ADD_BLOOB = "insert or ignore into blob (hash) values (?),"

@appcommand
def load(db, filename):
    with open(filename) as fp:
        items = [line.decode('utf-8', 'replace').strip().split('  ', 1)
                 for line in fp]
    db.executemany(IMPORT, items)
    db.commit()


def blocks(fp, blocksize=8192):
    return iter(functools.partial(fp.read, blocksize), b'')


def filehash(path):
    sha = hashlib.sha1()
    with open(path, mode='rb') as fp:
        for block in blocks(fp):
            sha.update(block)
    return sha.hexdigest()


def loadtree(db, base):
    base = os.path.abspath(base)
    for dirpath, dirnames, filenames in os.walk(base):
        blobs = {}
        links = set()
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            if os.path.islink(path):
                continue
            blobs[filename] = filehash(path)
