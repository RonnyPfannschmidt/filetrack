from .utils import appcommand, simplerows


REPOS = '''
    select distinct substr(name, 0, instr(name, :type))
    from fts_filename
    where name match :type
    order by name
'''


IMAGES = '''
    select
        basename(name) as basename,
        count(*) as c,
        listagg(name) as json
    from fts_filename
    where name match 'jpg'
    group by basename
    having c > 4
'''


@appcommand
def repos(db, type_):
    simplerows(db, REPOS, {'type': '.' + type_})


@appcommand
def images(db):
    simplerows(db, IMAGES, None)
