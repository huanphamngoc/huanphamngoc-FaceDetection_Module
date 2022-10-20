import urllib
from django.conf import settings
from django.test import TestCase
from rest_framework import serializers
import pyrebase
import io
from PIL import Image
import numpy as np
import cv2
import pickle

# Create your tests here.
from .serializers import SinhVienSerializer, AnhDangKySerializer, ChiTietLopHocSerializer

# serializer = AnhDangKySerializer()
# print(repr(serializer))

# firebaseConfig = settings.FIREBASE_CONFIGURE
# firebase = pyrebase.initialize_app(firebaseConfig)
# storage = firebase.storage()

# filepath = 'face_recognition_data/training_dataset/1.jpg'
# filename = 'Registration Images/Bang/demoimage.jpg'
# storage.child(filename).put(filepath)

# filename = 'Registration Images/Bang'
# print(storage.child(filename).get_url(None))

# file = storage.child(filename).download("", 'downloaded_images.jpg')
# print(file)

#READING FILE
# url = storage.child(filename).get_url(None)
# file = urllib.request.urlopen(url).read()
# image = Image.open(io.BytesIO(file)) #RGB
# image.save("PIL-image.jpg")
# image = np.array(Image.open(io.BytesIO(file))) #RGB
# print(image.shape)
# image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #Convert to BGR to work with opencv
# cv2.imwrite('cv2-image.jpg', image)
# _, jpeg = cv2.imencode('.jpg', image)
# print(cv2.imencode('.jpg', image)[1].tobytes())

# storage.child('Registration Images/Bang/demoimage5.jpg').put(cv2.imencode('.jpg', image)[1].tobytes())

#LISTING FILES
# path = 'Registration Images/'
# all_files = storage.list_files()
# print(all_files)


# for file in all_files:
#     try:
#         file.download_to_filename(datadir + file.name)
#     except:
#         print('Download Failed')

# dataset = pickle.load(open('Dataset\LT1\LT1_ImageDataset.pkl', 'rb'))
# print(dataset['images'].shape)
# print(dataset['classes'])
# print(len(dataset['classes']))
# print(dataset['student_names'])

from home.facedata import DatasetManagement
directory = f'Dataset/LT1'
dataset_management = DatasetManagement(directory)
dataset = dataset_management.create_face_dataset()
print(dataset['images'].shape)
print(dataset['classes'])
print(len(dataset['classes']))
print(dataset['student_names'])
