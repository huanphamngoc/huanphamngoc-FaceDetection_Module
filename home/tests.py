import imp
from django.test import TestCase

import keras
import pickle

from sklearn import metrics
from .transfer_learning import TransferLearning_CNN_SVM

# Create your tests here.

directory = f'Dataset/01'
cnn_model = keras.models.load_model(f'{directory}/01_CNN_Model.pkl')


dataset = pickle.load(open(f'{directory}/01_ImageDataset.pkl', 'rb'))

print(cnn_model.metrics_names)
# Đánh giá model với dữ liệu train
print(cnn_model.evaluate(dataset['images'], dataset['classes'], verbose=1))
# Đánh giá model với dữ liệu test set
print(cnn_model.evaluate(dataset['images'], dataset['classes'], verbose=1))

clf = pickle.load(open(f'{directory}/01_SVM_Model.pkl', 'rb'))

tfl = TransferLearning_CNN_SVM(cnn_model)
			
feature_matrix = tfl.cnn_extract_feature(dataset['images'])

y_pred = clf.predict(feature_matrix)

print("Accuracy: ", metrics.accuracy_score(dataset['classes'], y_pred))

#Precision and Recall for each class of Iris data set which includes setosa, versicolor, virginica
print("Precision: ", metrics.precision_score(dataset['classes'], y_pred, average=None))
print("Recall: ", metrics.recall_score(dataset['classes'], y_pred, average=None))