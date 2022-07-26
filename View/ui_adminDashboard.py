from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

from View.ui_historyDialog import Ui_HistoryDialog
from View.ui_newEmployeeDialog import Ui_newEmployeeDialog

import View.ui_dialog as ui



class Ui_AdminDialog(QDialog):
    def __init__(self,controller):
        super(Ui_AdminDialog, self).__init__()
        loadUi("View/pages/admin_dashboard.ui", self)
        self.controller=controller

        self.backbutton.clicked.connect(self.runSlot)
        self.employeebutton.clicked.connect(self.employeeSlot)
        self.gethistorybutton.clicked.connect(self.histotySlot)

    @pyqtSlot()
    def runSlot(self):
        self.close()
        self.homepageWindow_()

    def homepageWindow_(self):
        self._new_window = ui.Ui_Dialog(self.controller)
        self._new_window.show()

    @pyqtSlot()
    def employeeSlot(self):
        self.hide()
        self.newDataWindow_()

    def newDataWindow_(self):
        self._new_window = Ui_newEmployeeDialog(self.controller)
        self._new_window.show()

    @pyqtSlot()
    def histotySlot(self):
        self.close()
        self.historyWindow_()

    def historyWindow_(self):
        self.historyDataWindow_ = Ui_HistoryDialog(self.controller)
        self.historyDataWindow_.show()


