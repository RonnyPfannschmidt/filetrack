import click
from .utils import connect


@click.group()
@click.pass_context
@click.option('--auto-migrate', is_flag=True)
@click.option('--db', envvar='FILETRACK_DB')
def main(ctx, db, auto_migrate):
    ctx.obj = connect(db, auto_migrate)

    @ctx.call_on_close
    def close_db():
        ctx.obj.close()

    pass
