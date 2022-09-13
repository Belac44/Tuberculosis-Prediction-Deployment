import pickle
import numpy as np
from PIL import Image


class ModelBuild:
    def __init__(self):
        self.model = pickle.load(open('model.pkl', 'rb'))

    def process_image(self, image):
        img = Image.open(image)
        img = img.resize((150, 150))
        sRGB_array = np.asarray(img) / 255
        if len(sRGB_array) == 4:
            grey_vals = np.array([0.2126, 0.7152, 0.0722, 0])
        elif len(sRGB_array) == 3:
            grey_vals = np.array([0.2126, 0.7152, 0.0722])
        img_gray = sRGB_array @ grey_vals
        return img_gray.ravel().reshape(1,22500)


    def predict(self, features):
        return self.model.predict(features)
