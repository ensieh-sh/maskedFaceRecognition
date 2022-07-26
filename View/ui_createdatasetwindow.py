from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class Ui_Datasetwindow(QDialog):
    def __init__(self):
        super(Ui_Datasetwindow, self).__init__()
        loadUi("View/pages/createdatasetwindow.ui", self)
