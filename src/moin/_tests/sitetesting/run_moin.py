#!/usr/bin/env python

from glob import glob
import os
import shutil
from subprocess import run


def main():
    cwd = os.getcwd()
    try:
        os.chdir(os.path.dirname(__file__))
        coms = [
                ['moin', 'index-create', '-s', '-i'],
                ['moin', 'load-help', '-n', 'common'],
                ['moin', 'load-help', '-n', 'en'],
               ]
        for fn in glob('pages/*.meta'):
            fn_data = f'{fn[0:-5]}.data'
            coms.append(['moin', 'item-put', '-m', fn, '-d', fn_data])
        coms.append(['moin', 'index-build'])
        coms.append(['moin', 'run', '-p', '9080'])
        for com in coms:
            run(com)
    finally:
        shutil.rmtree('wiki')
        os.chdir(cwd)


if __name__ == '__main__':
    main()
