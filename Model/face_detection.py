from cv2 import cv2

class Face_detection:

    def __init__(self):
        self.face_cascade= cv2.CascadeClassifier('./prepared/haarcascade_frontalface_default.xml')

    def face_extractor(self,img):
        faces = self.face_cascade.detectMultiScale(img, 1.3, 8)

        if faces is ():
            return None

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            cropped_face = img[y:y + h, x:x + w]

        return cropped_face


