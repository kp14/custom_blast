__author__ = 'kp14'

import os
import subprocess

from atom.api import Atom, Unicode, Str, Range, Bool, List, Value, Int, Tuple, observe
import enaml
from enaml.qt.qt_application import QtApplication


def get_db_locations():
    try:
        # check environment variable
        blast_env =  os.environ['BLASTDB']
        paths = blast_env.split(';')
        return paths
    except KeyError, e:
        # need to return this as a list so that it can populate the drop-down menu
        return None


class CustomBlastDB(Atom):
    """Represents parameters of a BLAST database.

    """
    fasta = Unicode('test')
    query = Unicode('query')
    sp_only = Bool(False)
    target_name = Unicode()

    def run(self):
        paths = get_db_locations()

        try:
            result = subprocess.check_output(['makeblastdb', '-in', self.fasta, '-dbtype', 'prot', '-parse_seqids',
                                              '-title', self.target_name, '-out', self.target_name], cwd=paths[0],
                                              stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, e:
            result = e.output
        return unicode(result)


class CustomBlastSearch(Atom):
    """Represents parameters of a BLAST search.

    """
    fasta = Unicode()
    db = Unicode()
    available_dbs = List()

    def populate(self):
        try:
            paths = get_db_locations()
            result = ''
            for path in paths:
                print path
                if len(path) > 1:
                    dbs = subprocess.check_output(['blastdbcmd', '-list', path])
                    result = result + dbs
            raw_dbs = result.split('\n')
            # each line looks like: F:\path\to\db\db_name db_type -> db_name
            self.available_dbs = [os.path.basename(x.split()[0]) for x in raw_dbs[:-1]]
        except TypeError, e: # paths is None
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


if __name__ == '__main__':
    cbdb = CustomBlastDB()
    cbs = CustomBlastSearch()

    with enaml.imports():
        from bastdb_nb import Main

    app = QtApplication()
    view = Main(db=cbdb, bs=cbs)
    view.show()
    app.start()
