from keras.optimizer_v1 import Adam
from keras_preprocessing.image import ImageDataGenerator

from Model.generate_data import GenerateData
from Model.cnn_models import CNNModels
import tensorflow as tf

class CreateCNNModels:
    def __init__(self):
        self.generateDataModel=GenerateData()
        self.cnnModels=CNNModels()

    def create_face_recognition_model(self):
        (training_set,validation_set)=self.generateDataModel.train_Nomask_data()
        model=self.cnnModels.face_recognition_model()
        model.compile(loss='categorical_crossentropy',
                      optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
                      metrics=['accuracy'])

        r = model.fit_generator(training_set,
                                validation_data=validation_set,
                                epochs=100,
                                verbose=1,
                                )

        model.save('./createdModels/face_recognition.h5')


    def create_masked_face_recognition(self):
        (training_set, validation_set) = self.generateDataModel.train_masked_data()
        model=self.cnnModels.masked_face_recognition_model()
        model.compile(loss='categorical_crossentropy',
                      optimizer=tf.keras.optimizers.Adam(lr=0.0001),
                      metrics=['accuracy'])

        r = model.fit_generator(training_set,
                                validation_data=validation_set,
                                epochs=100,
                                verbose=1,
                                )

        model.save('./createdModels/face_recognition_with_mask.h5')


    def create_mask_detection(self):

        (trainX, testX, trainY, testY)=self.generateDataModel.train_mask_Nomask()
        aug = ImageDataGenerator(
            rotation_range=20,
            zoom_range=0.15,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            horizontal_flip=True,
            fill_mode="nearest")
        model=self.cnnModels.mask_detection()

        INIT_LR = 1e-4
        EPOCHS = 20
        BS = 32

        opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
        model.compile(loss="binary_crossentropy", optimizer=opt,
                      metrics=["accuracy"])

        print("[INFO] training head...")
        H = model.fit(
            aug.flow(trainX, trainY, batch_size=BS),
            steps_per_epoch=len(trainX) // BS,
            validation_data=(testX, testY),
            validation_steps=len(testX) // BS,
            epochs=EPOCHS)

        model.save('./createdModels/mask_detector.model')








