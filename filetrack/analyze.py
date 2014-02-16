from .utils import appcommand, simplerows


REPOS = '''
    select distinct substr(name, 0, instr(name, :type))
    from fts_filename
    where name match :type
    order by name
'''


@appcommand
def repos(db, type_):
    simplerows(db, REPOS, {'type': '.' + type_})
