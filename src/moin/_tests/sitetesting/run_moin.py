#!/usr/bin/env python

import click
from glob import glob
import logging
import os
import shutil
from subprocess import run

logger = logging.getLogger(__name__)


@click.command()
@click.option('--load-help/--no-load-help', default=True)
@click.option('--backup-wiki/--no-backup-wiki', default=False)
def main(load_help, backup_wiki):
    cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(__file__))
        coms = []
        coms.append(['moin', 'index-create', '-s', '-i'])
        if load_help:
            coms.append(['moin', 'load-help', '-n', 'common'])
            coms.append(['moin', 'load-help', '-n', 'en'])
            for fn in glob('pages/*.meta'):
                fn_data = f'{fn[0:-5]}.data'
                coms.append(['moin', 'item-put', '-m', fn, '-d', fn_data])
        coms.append(['moin', 'index-build'])
        coms.append(['moin', 'run', '-p', '9080'])
        for com in coms:
            run(com)
    finally:
        if backup_wiki:
            try:
                run(['moin', 'save', '--all-backends', 'True', '--file', 'wiki.moin'])
            except Exception as e:
                logger.warn(f'unable to backup: {repr(e)}')
        shutil.rmtree('wiki')
        os.chdir(cwd)


if __name__ == '__main__':
    main()
