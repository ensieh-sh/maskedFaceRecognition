from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QInputDialog, QMessageBox
from PyQt5 import uic
from View.ui_outputDialog import Ui_OutputDialog
from View.ui_adminDashboard import Ui_AdminDialog

class Ui_Dialog(QDialog):

    def __init__(self,controller):
        super(Ui_Dialog, self).__init__()
        uic.loadUi("View/pages/mainwindow.ui", self)
        self.controller=controller

        self.runbutton.clicked.connect(self.runSlot)

        self.adminbutton.clicked.connect(self.pups)



        self._new_window = None
        self.Videocapture_ = None


    def pups(self):
        text, ok = QInputDialog.getText(self, 'Admin Access', 'Enter password :')

        if ok:
            if(str(text)=='123456'):
                self.adminSlot()
            else :
                messege = QMessageBox.critical(self, "WARNING", "Wrong password ! try again ");



    def refreshAll(self):

        self.Videocapture_ = "0"

    @pyqtSlot()
    def runSlot(self):

        print("Clicked Run")
        self.refreshAll()
        print(self.Videocapture_)
        self.hide()  # hide the main window
        self.outputWindow_()  # Create and open new output window

    def outputWindow_(self):

        self._new_window = Ui_OutputDialog(self.controller)
        self._new_window.show()
        self._new_window.startVideo(self.Videocapture_)
        print("Video Played")

    @pyqtSlot()
    def adminSlot(self):
        self.hide()
        self.adminWindow_()

    def adminWindow_(self):
        self._new_window = Ui_AdminDialog(self.controller)
        self._new_window.show()



