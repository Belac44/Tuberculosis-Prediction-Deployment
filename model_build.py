import numpy as np
import cv2
from keras.models import model_from_json


class ModelBuild:
    def __init__(self):
        self.img = None
        self.model = self.make_model()

    def make_model(self):
        file = open("finalmodel.json", 'r')
        loaded_model_json = file.read()
        file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights("finalmodel.h5")
        return model


    def preprocess_image2(self, image):
        self.img = cv2.imread(str(image))
        self.img = cv2.resize(self.img, (28, 28))
        if self.img.shape[2] == 1:
            self.img = np.dstack([self.img, self.img, self.img])
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.img = np.array(self.img)
        self.img = self.img / 255
        return self.img.reshape(-1, 28, 28, 3)

    def predict(self, features):
        pred = self.model(features)
        return float(pred[0][0]), float(pred[0][1])
