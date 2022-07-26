from glob import glob

from keras.applications.mobilenet_v2 import MobileNetV2
from keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, Activation, GlobalAveragePooling2D, Lambda, \
    Input, BatchNormalization, AveragePooling2D
from keras.models import Model, Sequential
from keras.applications.vgg16 import VGG16
from Model.generate_data import GenerateData


class CNNModels:

    def __init__(self):
        self.generate_data_model = GenerateData()

    def face_recognition_model(self):
        IMAGE_SIZE = [224, 224]
        vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

        for layer in vgg.layers[:15]:
            layer.trainable = False

        folders = glob('Dataset/NoMask/train/*')
        num_classes = len(folders)

        FC_Head = self.face_recognition_layer_adder(vgg, num_classes)

        model = Model(inputs=vgg.input, outputs=FC_Head)

        return model

    def face_recognition_layer_adder(self, bottom_model, num_classes):
        top_model = bottom_model.output
        top_model = Conv2D(filters=20, kernel_size=7, activation='relu', input_shape=(224, 224, 3),
                           padding='same')(top_model)
        top_model = MaxPooling2D(pool_size=2)(top_model)

        top_model = Conv2D(filters=54, kernel_size=5, activation='relu', input_shape=(224, 224, 3),
                           padding='same')(top_model)

        top_model = Flatten()(top_model)

        top_model = Dense(1024, activation='relu')(top_model)
        top_model = BatchNormalization()(top_model)

        top_model = Dense(512, activation='relu')(top_model)
        top_model = BatchNormalization()(top_model)

        top_model = Dropout(0.5)(top_model)

        top_model = Dense(num_classes, activation='softmax')(top_model)
        return top_model

    def masked_face_recognition_model(self):
        IMAGE_SIZE = [224, 224]
        vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

        for layer in vgg.layers[:15]:
            layer.trainable = False

        folders = glob('Dataset/Masked/train/*')
        num_classes = len(folders)
        FC_Head = self.masked_face_recognition_layer_adder(vgg, num_classes)

        model = Model(inputs=vgg.input, outputs=FC_Head)

        return model

    def masked_face_recognition_layer_adder(self, bottom_model, num_classes):

        top_model = bottom_model.output

        top_model = Flatten()(top_model)

        top_model = Dense(1024, activation='relu')(top_model)
        top_model = BatchNormalization()(top_model)

        top_model = Dropout(0.25)(top_model)

        top_model = Dense(512, activation='relu')(top_model)

        top_model = Dropout(0.5)(top_model)

        top_model = Dense(num_classes, activation='softmax')(top_model)
        return top_model

    def mask_detection(self):

        baseModel = MobileNetV2(weights="imagenet", include_top=False,
                                input_tensor=Input(shape=(224, 224, 3)))

        FC_Head = self.mask_detection_layer_adder(baseModel)

        model = Model(inputs=baseModel.input, outputs=FC_Head)

        for layer in baseModel.layers:
            layer.trainable = False

        return model

    def mask_detection_layer_adder(self, bottom_model):

        num_classes = 2

        top_model = bottom_model.output

        top_model = AveragePooling2D(pool_size=(7, 7))(top_model)

        top_model = Flatten(name="flatten")(top_model)

        top_model = Dense(128, activation='relu')(top_model)
        top_model = Dropout(0.5)(top_model)

        top_model = Dense(num_classes, activation='softmax')(top_model)

        return top_model
