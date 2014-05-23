__author__ = 'kp14'

import enaml
from enaml.qt.qt_application import QtApplication

from models import db, run


if __name__ == '__main__':
    cbdb = db.CustomBlastDB()
    cbs = run.CustomBlastSearch()

    with enaml.imports():
        from gui.gui import Main

    app = QtApplication()
    view = Main(db=cbdb, bs=cbs)
    view.show()
    app.start()
