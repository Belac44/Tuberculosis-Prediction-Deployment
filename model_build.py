import pickle
import numpy as np
from PIL import Image
from skimage.color import rgb2gray

class ModelBuild:
    def __init__(self):
        self.model = pickle.load(open('model.pkl', 'rb'))

    def process_image(self, image):
        img = Image.open(image)
        img = img.resize((150, 150))
        sRGB_array = np.asarray(img)
        img_gray = rgb2gray(sRGB_array)
        img_gray = img_gray/255
        return img_gray.ravel().reshape(1, 22500)


    def predict(self, features):
        return self.model.predict(features)
