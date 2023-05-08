from sklearn.metrics.pairwise import cosine_similarity
import numpy as np # linear algebra
import cv2 # opencv
from keras.models import load_model

# load the facenet model
facenet_model = load_model("C:\Users\ACER\OneDrive\Documents\Kì 2 - Năm 3\TTCS\Timekeeping-main\facenet_keras.h5")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

IMG_SIZE = 160

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

def sklearn_cosine(x,y):
    return cosine_similarity(x, y)

print(get_embedding_bydir('/home/baocongidol/WorkSpace/ttcs/media/elton_john.jpg',facenet_model, face_cascade ).shape)

