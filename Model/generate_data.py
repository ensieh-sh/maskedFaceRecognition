import json
import os
import numpy as np
from imutils import face_utils

import cv2
import dlib as dlib
from keras_preprocessing.image import ImageDataGenerator, load_img, img_to_array
from Model.face_detection import Face_detection
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

import numpy as np
import os


class GenerateData:
    def __init__(self):
        self.trainNoMaskPath = './Dataset/NoMask/train'
        self.trainMaskedPath = './Dataset/Masked/train'
        self.trainMaskNomaskPath='./Dataset/mask_detection'

        self.face_detection_model = Face_detection()

    def train_Nomask_data(self):
        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=45,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           width_shift_range=0.3, height_shift_range=0.3,
                                           horizontal_flip=True
                                           , fill_mode='nearest', validation_split=0.2)

        training_set = train_datagen.flow_from_directory(self.trainNoMaskPath,
                                                         target_size=(224, 224),
                                                         batch_size=32,
                                                         class_mode='categorical',
                                                         subset='training')

        validation_set = train_datagen.flow_from_directory(self.trainNoMaskPath,
                                                           target_size=(224, 224),
                                                           batch_size=32,
                                                           class_mode='categorical',
                                                           subset='validation')

        class_dict = validation_set.class_indices
        classes = {}
        for key, value in class_dict.items():
            classes[value] = key

        with open('classes.txt', 'w') as file:
            file.write(json.dumps(classes))

        return (training_set, validation_set)

    def train_masked_data(self):

        train_datagen = ImageDataGenerator(rescale=1. / 255,
                                           rotation_range=45,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           width_shift_range=0.3, height_shift_range=0.3,
                                           horizontal_flip=True
                                           , fill_mode='nearest', validation_split=0.2)

        training_set = train_datagen.flow_from_directory(self.trainMaskedPath,
                                                         target_size=(224, 224),
                                                         batch_size=32,
                                                         class_mode='categorical',
                                                         subset='training')

        validation_set = train_datagen.flow_from_directory(self.trainMaskedPath,
                                                           target_size=(224, 224),
                                                           batch_size=32,
                                                           class_mode='categorical',
                                                           subset='validation')

        return (training_set, validation_set)

    def train_mask_Nomask(self):
        DIRECTORY = self.trainMaskNomaskPath
        CATEGORIES = ["with_mask", "without_mask"]

        data = []
        labels = []

        for category in CATEGORIES:
            path = os.path.join(DIRECTORY, category)
            for img in os.listdir(path):
                img_path = os.path.join(path, img)
                image = load_img(img_path, target_size=(224, 224))
                image = img_to_array(image)
                image = preprocess_input(image)

                data.append(image)
                labels.append(category)

        lb = LabelBinarizer()
        labels = lb.fit_transform(labels)
        labels = to_categorical(labels)

        data = np.array(data, dtype="float32")
        labels = np.array(labels)

        (trainX, testX, trainY, testY) = train_test_split(data, labels,
                                                          test_size=0.20, stratify=labels, random_state=42)

        return  (trainX, testX, trainY, testY)


    def getClasses(self):
        classes = json.load(open("classes.txt"))
        return classes


    def collect_images(self, name):

        if not os.path.exists(os.path.join(self.trainNoMaskPath, name)):
            os.makedirs(os.path.join(self.trainNoMaskPath, name))

        new_train_path = os.path.join(self.trainNoMaskPath, name)

        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            face=self.face_detection_model.face_extractor(frame)
            if face is not None:
                count += 1
                face = cv2.resize(face, (400, 400))

                file_name_path = new_train_path + '/' + 'f' + str(count) + '.jpg'
                # print(file_name_path)
                cv2.imwrite(file_name_path, face)

                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)

            else:
                print("Face not found")
                pass

            if cv2.waitKey(1) == 13 or count == 200:
                break

        cap.release()
        cv2.destroyAllWindows()

        print("collecting samples complete")

    def add_mask(self, name):

        print('start creating mask data')

        new_train_path = os.path.join(self.trainMaskedPath, name)
        train_path = os.path.join(self.trainNoMaskPath, name)

        if not os.path.exists(os.path.join(self.trainMaskedPath, name)):
            os.makedirs(os.path.join(self.trainMaskedPath, name))


        images = [os.path.join(train_path, f) for f in os.listdir(train_path) if
                  os.path.isfile(os.path.join(train_path, f))]
        j = 0
        num = (len(images))

        while j < num:
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor('./prepared/shape_predictor_68_face_landmarks.dat')
            image = cv2.imread(images[j])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rects = detector(gray, 1)
            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                x, y = shape[1]
                x1, y1 = shape[30]
                x2, y2 = shape[15]
                x3, y3 = shape[14]
                x4, y4 = shape[12]
                x5, y5 = shape[10]
                x6, y6 = shape[9]
                x7, y7 = shape[8]
                x8, y8 = shape[6]
                x9, y9 = shape[4]
                x10, y10 = shape[2]

                pts = np.array([[x, y], [x1, y1], [x2, y2], [x3, y3],
                                [x4, y4], [x5, y5], [x6, y6], [x7, y7],
                                [x8, y8], [x9, y9], [x10, y10]])
                cv2.fillPoly(image, [pts], color=(0, 0, 0))

            new_file_path = new_train_path + '/' + 'masked%s.jpg' % (j)
            cv2.imwrite(new_file_path, image)
            j += 1

        print('created mask data comlete')
