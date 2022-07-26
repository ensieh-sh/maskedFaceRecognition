from keras.models import load_model
import numpy as np
from Model.generate_data import GenerateData


class Face_recognition:
    def __init__(self):
       self.faceRecognitionPath='./createdModels/face_recognition.h5'
       self.maskedFaceRecognitionPath='./createdModels/face_recognition_with_mask.h5'
       self.faceRecognitionModel=load_model(self.faceRecognitionPath)
       self.maskedFaceRecognitionModel=load_model(self.maskedFaceRecognitionPath)
       self.generate_data_model=GenerateData()

    def face_recognition(self, img_array, masked):

        classes = self.generate_data_model.getClasses()

        if (masked):
            predict = self.maskedFaceRecognitionModel.predict(img_array)
            x = np.argmax(predict, axis=-1)
            name = classes.get(str(int(x)))

        else:
            predict = self.faceRecognitionModel.predict(img_array)
            x = np.argmax(predict, axis=-1)
            name = classes.get(str(int(x)))

        return name
