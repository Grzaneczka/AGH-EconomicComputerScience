import sys

from PyQt5.QtWidgets import QApplication

from gui.load_dialog import LoadDialog
from gui.window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create dialog for loading warehouse
    load_dialog = LoadDialog()
    load_dialog.exec_()

    # stop if no warehouse was created stop app
    if load_dialog.warehouse is None:
        sys.exit()

    # create main window
    window = MainWindow(load_dialog.warehouse)
    window.show()

    sys.exit(app.exec_())
