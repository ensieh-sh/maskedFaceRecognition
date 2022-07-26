from datetime import datetime
from PyQt5.QtCore import QDate, pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
import View.ui_dialog as ui
from cv2 import cv2
import Controller.main_controller as MainController
import numpy as np

class Ui_OutputDialog(QDialog):
    def __init__(self,controller):
        super(Ui_OutputDialog, self).__init__()
        loadUi("View/pages/outputwindow.ui", self)
        self.MainController = controller


        now = QDate.currentDate()
        current_date = now.toString('ddd dd MMMM yyyy')
        current_time = datetime.now().strftime("%I:%M %p")
        self.datelabel.setText(current_date)
        self.timelabel.setText(current_time)

        self.backbutton.clicked.connect(self.runSlot)
        self.flag=None
        self._new_window = None

        self.image = None

    def refreshAll(self):
        # self.Videocapture_ = None
        self.flag=True
        cv2.VideoCapture(0).release()
        cv2.destroyAllWindows()


    @pyqtSlot()
    def runSlot(self):
        self.refreshAll()
        print("Clicked Run")
        self.close()
        self.homepageWindow_()

    def homepageWindow_(self):
        self.capture.release()
        self._new_window = ui.Ui_Dialog(self.MainController)
        self._new_window.show()

    @pyqtSlot()
    def startVideo(self, camera_name):

        if len(camera_name) == 1:
            self.capture = cv2.VideoCapture(int(camera_name))
        else:
            self.capture = cv2.VideoCapture(camera_name)

        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(20)  # emit the timeout() signal at x=40ms




    def face_rec_(self, frame):

        def add_show(name, db_label):
            if self.Clockinbutton.isChecked():
                self.Clockinbutton.setEnabled(False)
                ButtonReply = QMessageBox.question(self, 'Welcome  ' + name, ' ! Do you want to login?',
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if ButtonReply == QMessageBox.Yes:
                    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                    self.MainController.insert(name,time,db_label,'login')

                    self.Clockinbutton.setChecked(False)

                    self.namelabel.setText(name)
                    self.masklabel.setText(db_label)
                    self.statuslabel.setText("login")
                    self.hourslabel.setText('-')
                    self.minlabel.setText('-')

                    self.Clockinbutton.setEnabled(True)

                else:
                    self.Clockinbutton.setEnabled(True)


            elif self.Clockoutbutton.isChecked():

                self.Clockoutbutton.setEnabled(False)

                ButtonReply = QMessageBox.question(self, 'bye  ' + name, '! Do you want to logout?',
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if ButtonReply == QMessageBox.Yes:
                    time = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                    self.MainController.insert(name,time,db_label,'logout')


                    self.Clockoutbutton.setChecked(False)

                    clockinTime = self.MainController.last_login(name)
                    clockinTime = datetime.strptime(clockinTime, '%y/%m/%d %H:%M:%S')

                    CheckOutTime = datetime.strptime((datetime.now().strftime("%y/%m/%d %H:%M:%S")),
                                                     '%y/%m/%d %H:%M:%S')

                    self.ElapseHours = (CheckOutTime - clockinTime)
                    print('diff ', self.ElapseHours)
                    self.minlabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60) % 60) + 'm')
                    self.hourslabel.setText("{:.0f}".format(abs(self.ElapseHours.total_seconds() / 60 ** 2)) + 'h')

                    self.namelabel.setText(name)
                    self.masklabel.setText(db_label)
                    self.statuslabel.setText("logout")

                    self.Clockoutbutton.setEnabled(True)
                else:
                    self.Clockoutbutton.setEnabled(True)

        (locs, preds) = self.MainController.mask_predict(frame)

        for (box, pred) in zip(locs, preds):

            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            if mask>withoutMask:
                label="has Mask"
                color=(0,255,0)
            else:
                label="No Mask"
                color=(0,0,255)

            db_label = label

            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

            img_array = self.MainController.face_toArray(frame)

            if (mask < withoutMask):


                name = self.MainController.face_rec(img_array,False)
                # print(name)
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else :

                name = self.MainController.face_rec(img_array,True)
                # print(name)
                cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)



        add_show(name, db_label)

        return (frame, db_label, name)


    def update_frame(self):
        if (self.flag==None):

            ret, self.image = self.capture.read()
            cv2.imwrite('test.jpg',self.image)
            self.displayImage(self.image, 1)
        else :
            pass

    def displayImage(self, image, window=1):

        image = cv2.resize(image, (400, 400))
        try:
            image, db_label, name = self.face_rec_(image)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.imgLabel.setPixmap(QPixmap.fromImage(outImage))
            self.imgLabel.setScaledContents(True)


