from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Ui_Trainingwindow(QDialog):
    def __init__(self):
        super(Ui_Trainingwindow, self).__init__()
        loadUi("View/pages/Trainingwindow.ui", self)
