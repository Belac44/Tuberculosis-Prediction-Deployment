import numpy as np
import joblib
import cv2

class ModelBuild:
    def __init__(self):
        self.model = joblib.load("model_main.pkl")

    def preprocess_image2(image):
        img = cv2.imread(str(image))
        img = cv2.resize(img, (28, 28))
        if img.shape[2] == 1:
            img = np.dstack([img, img, img])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.array(img)
        img = img / 255
        return img.reshape(-1, 28, 28, 3)


    def predict(self, features):
        pred = self.model(features)
        return (float(pred[0][0]), float(pred[0][1]))
