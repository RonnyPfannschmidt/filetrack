from . import appcommand


REPOS = '''
    select distinct substr(name, 0, instr(name, :type))
    from fts_filename
    where name match :type
    order by name
'''


@appcommand
def repos(db, type_):
    results = db.execute(REPOS, {'type': '.' + type_})
    for item in results:
        print(item[0])
