from datetime import datetime
from PyQt5.QtCore import QDate, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import View.ui_dialog as ui

class Ui_HistoryDialog(QDialog):
    def __init__(self,controller):
        super(Ui_HistoryDialog, self).__init__()
        loadUi("View/pages/Doc.ui", self)
        self.controller=controller

        self.backbutton.clicked.connect(self.runSlot)

        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.now().strftime("%I:%M %p")
        self.datelabel.setText(current_date)
        self.timelabel.setText(current_time)

        self.Submitbutton.clicked.connect(self.find_data)

        self._new_window = None

    @pyqtSlot()
    def runSlot(self):
        self.close()
        self.adminWindow_()

    def adminWindow_(self):

        self._new_window = ui.Ui_AdminDialog(self.controller)
        self._new_window.show()

    def find_data(self):

        name = self.nameEdit.text()

        if (name):
            data =self.controller.select_by_name(name)
            self.tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.tableWidget.insertRow(row)
                for column, item in enumerate(form):
                    # print(str(item))
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

        # else :
        #     messege = 'please enter name '
        #     QMessageBox.about(self, "WARNING", messege)

        datefield=self.datefield.text()

        if(datefield):

            data = self.controller.select_by_date(datefield)
            self.tableWidget.setRowCount(0)
            for row, form in enumerate(data):
                self.tableWidget.insertRow(row)
                for column, item in enumerate(form):
                    # print(str(item))
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))






