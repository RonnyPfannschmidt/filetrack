from filetrack.load import filehash, walk_filesets


def test_filehash(tmpdir):
    fp = tmpdir.ensure('fmpfile')
    assert filehash(str(fp)) == fp.computehash('sha1')


def test_walk_fileset(tmpdir):
    fp = tmpdir.ensure('tmpfile')
    tmpdir.ensure('test', dir=1)
    expected = fp.computehash('sha1')
    (root, subdirs) = walk_filesets(str(tmpdir))
    print (root)
    assert root.blobs['tmpfile'] == expected


def test_load_fileset(db):
    pass
