import numpy as np
import joblib
import cv2


class ModelBuild:
    def __init__(self):
        self.model = joblib.load("model_main.pkl")
        self.img = None

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
