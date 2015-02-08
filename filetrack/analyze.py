from .utils import simplerows
import click
from .cli import main


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


@main.command()
@click.pass_obj
@click.argument('kind')
def repos(db, kind):
    simplerows(db, REPOS, {'type': '.' + kind})


@main.command()
@click.pass_obj
def images(db):
    simplerows(db, IMAGES, None)
