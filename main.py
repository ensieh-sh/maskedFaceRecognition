import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from Controller.main_controller import MainController
from View.ui_dialog import Ui_Dialog
from Model.database import DatabaseModel

from View.pages import myrecog


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.db_model=DatabaseModel()
        self.main_controller = MainController(self.db_model)
        self.main_view = Ui_Dialog(self.main_controller)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

