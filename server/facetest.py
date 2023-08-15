import cv2
import os
import pickle
import numpy as np
import pickle

import keras.utils as image
from keras_vggface import utils
from tensorflow.keras.models import load_model

class Conv_network:
    def __init__ (self, image_width, image_height):
        self.test_setup()
        self.image_width = image_width
        self.image_height = image_height
        self.screen_width = 1280
        self.screen_height = 720

    def test_setup(self):
        # load trained model
        self.model = load_model(r'.\server/resources/model.h5')

        # load the training labels
        face_label_filename = f'./server/resources/face-labels.pickle'
        with open(face_label_filename, "rb") as f:
            class_dictionary = pickle.load(f)

        self.class_list = [value for _, value in class_dictionary.items()]
        print(self.class_list)

    def predict_face(self, filename):
        # Predicting the faces
        facecascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # load the image
        imgtest = cv2.imread(filename, cv2.IMREAD_COLOR)
        image_array = np.array(imgtest, "uint8")

        # get the faces detected in the image
        faces = facecascade.detectMultiScale(imgtest, scaleFactor=1.1, minNeighbors=5)
        print(len(faces))
        # if not exactly 1 face is detected, skip this photo
        if len(faces) >= 1:
            print(f"Found {len(faces)} faces")
            print(f'---We need exactly 1 face; photo skipped---')
            print()
            # continue

            for (x_, y_, w, h) in faces[:1]:
                # resize the detected face to 224x224
                size = (self.image_width, self.image_height)
                roi = image_array[y_: y_ + h, x_: x_ + w]
                resized_image = cv2.resize(roi, size)

                # prepare the image for prediction
                x = image.img_to_array(resized_image)
                x = np.expand_dims(x, axis=0)
                x = utils.preprocess_input(x, version=1)

                # making prediction
                predicted_prob = self.model.predict(x)
                result_class = self.class_list[predicted_prob[0].argmax()]
                print(predicted_prob)
                print(predicted_prob[0].argmax())
                print("Predicted face: " + result_class)
                print("============================\n")
                
            return {"result": "Approved", "class": result_class} if result_class != "Unknown" else {"result": "Reproved", "class": result_class}

        elif len(faces) == 0:
            return {"result": "No faces found", "class": "None"}
        
    