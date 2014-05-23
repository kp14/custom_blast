__author__ = 'kp14'

import os
import subprocess

from atom.api import Atom, Unicode, Bool

from helpers import env

class CustomBlastDB(Atom):
    """Represents parameters of a BLAST database.

    """
    fasta = Unicode('test')
    query = Unicode('query')
    sp_only = Bool(False)
    target_name = Unicode()

    def run(self):
        paths = env.get_db_locations()

        try:
            result = subprocess.check_output(['makeblastdb', '-in', self.fasta, '-dbtype', 'prot', '-parse_seqids',
                                              '-title', self.target_name, '-out', self.target_name], cwd=paths[0],
                                              stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError, e:
            result = e.output
        return unicode(result)

