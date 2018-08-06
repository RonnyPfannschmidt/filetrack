import lzma


def fetch_entries(path):

    if path.suffix == '.xz':
        fp = lzma.open(str(path))
    else:
        raise ValueError(path.suffix)
    with fp:
        yield from normalize(
            x.decode('utf-8').strip('\n').split('\t') for x in fp)


def fetch_all(paths):
    for path in paths:
        yield from fetch_entries(path)


def fetch_sample(paths, n=2):
    paths = sorted(paths, key=lambda p: p.stat().st_size)[:n]
    yield from fetch_all(paths)


def normalize(elements):
    for repo, name, size, checksum in elements:
        yield repo, name, int(size) if size else None, checksum
