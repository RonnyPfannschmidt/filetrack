import os
import hashlib
import functools
from itertools import starmap
from collections import namedtuple

from .cli import main
import click

FileSet = namedtuple('FileSet', 'path dirnames blobs links')


IMPORT = "insert or ignore into filename_blob(blob, name) values(?, ?)"
ADD_BLOOB = "insert or ignore into blob (hash) values (?)"


@main.command()
@click.pass_obj
@click.argument('file', type=click.File(encoding='utf-8', errors='replace'))
def load(db, file):
    items = [line.strip().split(u'  ', 1) for line in file]
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


def splice(path, filenames,
           _islink=os.path.islink,
           _filehash=filehash):
    blobs = {}
    links = set()
    for filename in filenames:
        path = os.path.join(path, filename)
        if _islink(path):
            links.add(filename)
        else:
            blobs[filename] = _filehash(path)
    return blobs, links


def compute_fileset(path, dirnames, filenames, _splice=splice):

    blobs, links = _splice(path, filenames)
    return FileSet(path, dirnames, blobs, links)


def walk_filesets(base):
    return starmap(compute_fileset, os.walk(base))


def insert_fileset(db, fileset):
    pass


@main.command()
@click.pass_context
@click.argument('base')
def loadtree(ctx, base):
    base = os.path.abspath(base)
    for fileset in walk_filesets(base):
        insert_fileset(ctx.db, *fileset)
