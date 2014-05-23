__author__ = 'kp14'

import subprocess

from atom.api import Atom, Unicode, List

from helpers import env

class CustomBlastSearch(Atom):
    """Represents parameters of a BLAST search.

    """
    fasta = Unicode()
    db = Unicode()
    available_dbs = List()

    def populate(self):
        try:
            paths = env.get_db_locations()
            result = ''
            for path in paths:
                print path
                if len(path) > 1:
                    dbs = subprocess.check_output(['blastdbcmd', '-list', path])
                    result += dbs
            raw_dbs = result.split('\n')
            # each line looks like: F:\path\to\db\db_name db_type -> db_name
            self.available_dbs = [os.path.basename(x.split()[0]) for x in raw_dbs[:-1]]
        except TypeError, e:  # paths is None
            # need to return this as a list so that it can populate the drop-down menu
            self.available_dbs = ['None, check variable: {}'.format(e.message)]

    def run(self):
        print self.fasta
        print self.db
        try:
            result = subprocess.check_output(['blastp',
                                              '-query', self.fasta,
                                              '-db', self.db,
                                              '-out', './tmp/blast.out'],
                                             stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, e:
            result = e.output
        print unicode(result)