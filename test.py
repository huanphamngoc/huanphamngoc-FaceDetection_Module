

import base64

import pickle
import numpy as np
import base64
import cv2
import io
import pickle

directory = f'Dataset/LT1'
classes = f'LT1'
dataset = pickle.load(open(f'{directory}/{classes}_ImageDataset.pkl', 'rb'))
print(dataset.keys())
images = dataset['images']
labels = dataset['classes']
class_names = dataset['student_names']
Student_ids = dataset['student_ids']
print(images.shape)
print(labels.shape)
# print(images)
print(class_names)
# print(labels)
a = []
# a = np.array(a)
labels = list(labels)
# print(type(labels))
tmp = len(labels)
for i in range(tmp):
    if labels[i] != 0:
        a.append(labels[i])
print(np.array(a))