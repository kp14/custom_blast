__author__ = 'kp14'

import os

def get_db_locations():
    """Extract locations for BLAST dbs from environment variable BLASTDB

    """
    try:
        blast_env = os.environ['BLASTDB']
        paths = blast_env.split(';')
        return paths
    except KeyError:
        # need to return this as a list so that it can populate the drop-down menu
        return None
