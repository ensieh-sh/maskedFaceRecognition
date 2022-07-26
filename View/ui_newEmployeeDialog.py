from datetime import datetime
from threading import Timer

from PyQt5.QtCore import pyqtSlot, QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import uic
from PyQt5.uic import loadUi
import View.ui_dialog as ui
from View.ui_trainingDialog import Ui_Trainingwindow
from View.ui_createdatasetwindow import Ui_Datasetwindow


class Ui_newEmployeeDialog(QDialog):
    def __init__(self, controller):
        super(Ui_newEmployeeDialog, self).__init__()
        loadUi("View/pages/newdatawindow.ui", self)
        self.controller = controller

        self.t = Timer(1.0, self.start_training)

        self.t1 = Timer(1.0, self.start_addMask)

        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.now().strftime("%I:%M %p")
        self.datelabel.setText(current_date)
        self.timelabel.setText(current_time)

        self.setphotobutton.clicked.connect(self.get_data)

        self.Submitbutton.clicked.connect(self.open_trainingwindow)

        self.backbutton.clicked.connect(self.runSlot)

        self._new_window = None

        self.train_window = None
        self.dataset_window = None

        self.name=None

        self.image = None

    @pyqtSlot()
    def runSlot(self):

        self.close()
        self.adminWindow_()

    def adminWindow_(self):

        self._new_window = ui.Ui_AdminDialog(self.controller)
        self._new_window.show()

    def get_data(self):

        if self.setphotobutton.isChecked():

            self.setphotobutton.setEnabled(False)

            self.name = self.nameEdit.text()
            exists = self.controller.contain_name(self.name)

            if (exists):

                self.setphotobutton.setChecked(False)

                messege = QMessageBox.about(self, "WARNING", "this name used please enter new name !");

                self.setphotobutton.setEnabled(True)

            else:
                self.setphotobutton.setChecked(False)

                self.controller.collect_images(self.name)

                self.open_datasetwindow()

                self.setphotobutton.setEnabled(True)

    def open_trainingwindow(self):
        self.train_window = Ui_Trainingwindow()
        self.train_window.show()
        self.t.start()

    def open_datasetwindow(self):
        self.dataset_window = Ui_Datasetwindow()
        self.dataset_window.show()
        self.t1.start()

    def start_addMask(self):

        self.controller.start_add_mask(self.name)
        self.dataset_window.close()




    def start_training(self):

        if self.Submitbutton.isChecked():
            self.Submitbutton.setEnabled(False)

            self.controller.training_model()

            self.train_window.close()


            self.Submitbutton.setChecked(False)

            self.Submitbutton.setEnabled(True)
