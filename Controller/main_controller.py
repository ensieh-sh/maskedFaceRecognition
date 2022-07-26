import cv2
from PIL import Image
import numpy as np

from Model.database import DatabaseModel
from Model.mask_prediction import Mask_prediction
from Model.face_detection import Face_detection
from Model.face_recognition import Face_recognition
from Model.generate_data import GenerateData
from Model.create_models import CreateCNNModels
import tensorflow as tf

class MainController:
    def __init__(self,dbModel):
        self.database_model =dbModel
        self.mask_prediction_model = Mask_prediction()
        self.face_detection_model=Face_detection()
        self.face_recognition_model=Face_recognition()
        self.generate_data_model=GenerateData()
        self.create_CNN_Models_model=CreateCNNModels()



    def mask_predict(self,frame):
        (locs,preds)=self.mask_prediction_model.detect_and_predict_mask(frame)

        return (locs,preds)

    def face_extractor(self,frame):
         cropped_face=self.face_detection_model.face_extractor(frame)

         return cropped_face

    def face_toArray(self,face):
        face = 'test.jpg'
        # im = Image.fromarray(face, 'RGB')
        # img_array = np.array(im)
        # img_array = np.expand_dims(img_array, axis=0)
        face = tf.keras.preprocessing.image.load_img(face, target_size=(224, 224))
        input_arr=tf.keras.preprocessing.image.img_to_array(face)
        input_arr = np.array([input_arr])
        img_array = input_arr.astype('float32') / 255.

        return img_array

    def face_rec(self,img_array,masked):
        name=self.face_recognition_model.face_recognition(img_array,masked)
        return name


    def insert(self,name,time,mask,state):
        self.database_model.insert_attendance(name,time,mask,state)

    def last_login(self,name):
        row=self.database_model.select_last_login_by_name(name)

        return row.get('time')

    def select_by_name(self,name):
        rows=self.database_model.select_all_by_name(name)

        return rows

    def contain_name(self,name):
        classes=self.generate_data_model.getClasses()
        if (name in classes.values()):
            exist=True
        else:
            exist=False

        return exist

    def collect_images(self,name):
        self.generate_data_model.collect_images(name)

    def training_model(self):
       self.create_CNN_Models_model.create_face_recognition_model()
       self.create_CNN_Models_model.create_masked_face_recognition()

    def start_add_mask(self,name):
        self.generate_data_model.add_mask(name)

    def select_by_date(self,date):

        rows=self.database_model.select_all_date(date)

        return rows







