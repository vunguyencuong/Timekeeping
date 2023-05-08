# import cv2 # opencv
# img = cv2.imread("C:\\Users\\ACER\\lionel-messi-16710055844x3.jpg")
# print(img)

import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# constants
IMG_SIZE = 160
FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
FACENET_MODEL = load_model('facenet_keras.h5')

def get_embedding(model, face):
    # scale pixel values
    face = face.astype('float32')
    # standardization
    mean, std = face.mean(), face.std()
    face = (face-mean)/std
    # transfer face into one sample (3 dimension to 4 dimension)
    sample = np.expand_dims(face, axis=0)
    # make prediction to get embedding
    
    yhat = model.predict(sample)
    return yhat[0]

def extract_face_ver2(filename, face_cascade):
    img = cv2.imread(filename)
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    faces_array = []
    for (x,y,w,h) in faces:
        crop = img_array[y:y+h, x:x+w]
        crop = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
        crop = crop.astype('float32')
        # standardization
        mean, std = crop.mean(), crop.std()
        crop = (crop-mean)/std
        # transfer face into one sample
        sample = np.expand_dims(crop, axis=0)
        faces_array.append(sample)
    return faces_array

def get_embedding_bydir(filename, facenet_model, face_cascade):
    # load the photo and extract the face
    face = extract_face_ver2(filename=filename,face_cascade = face_cascade)[0][0]
    emd = get_embedding(facenet_model, face)
    return emd

def predict_face():
    # open file dialog to select image
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    # get face embedding
    embedding = get_embedding_bydir(filename, FACENET_MODEL, FACE_CASCADE)
    # display prediction
    prediction_label.config(text="Face embedding: {}".format(embedding))

# create GUI
root = tk.Tk()
root.title("Face Recognition")
root.geometry("300x100")

# create widgets
select_image_button = tk.Button(root, text="Select Image", command=predict_face)
prediction_label = tk.Label(root, text="Face embedding: ")

# add widgets to GUI
select_image_button.pack()
prediction_label.pack()

# start GUI loop
root.mainloop()