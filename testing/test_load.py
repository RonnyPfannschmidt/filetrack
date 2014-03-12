from filetrack.load import filehash

def test_filehash(tmpdir):
    fp = tmpdir.ensure('fmpfile')
    assert filehash(str(fp)) == fp.computehash('sha1')


