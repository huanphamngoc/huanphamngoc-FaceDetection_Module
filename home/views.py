import pickle
import numpy as np
from django.conf import settings
from django.shortcuts import render
from sklearn.model_selection import cross_validate

from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from sklearn import metrics, svm

from .facedata import DatasetManagement
from .cnn import CNN
from .transfer_learning import TransferLearning_CNN_SVM
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold



class HomeAPIView(APIView):
	'''Home View'''
	template_name = 'home/index.html'

	def get(self, request, format=None):
		"""Trả về Home Template"""
		return render(request, self.template_name, {})

class ModelsTrainingAPI(APIView):
	'''Model Training View: Lớp này kích hoạt khi training model'''

	def put(self, request):
		"""Hàm training model: PUT Method"""
		try:
			directory = f'Dataset/LT1' #Tạo đường dẫ tới theo lớp học
			classes = f'LT1'
			#Tạo đối tượng thao tác dữ liệu
			dataset_management = DatasetManagement(directory) 

			#Tạo dataset
			dataset = dataset_management.create_face_dataset()
			
			# dataset = pickle.load(open('D:\my_project\Awesome-Guys\Dataset\LT1\LT1_ImageDataset.pkl','rb'))

			print(dataset.keys())
			images = dataset['images']
			labels = dataset['classes']
			class_names = dataset['student_names']
			print(images.shape)
			print(labels.shape)
			print(class_names)
			print(labels)
			#Tạo mô hình CNN
   
			cnn_model = CNN((120, 80, 3), len(dataset['student_names'])).cnn_model()

			#Hiển thị thông tin mô hình CNN
			cnn_model.summary()
			datagen = ImageDataGenerator(
			zoom_range=[1.0,1.1],
			# brightness_range=[0.2,1.0],
			# rotation_range=10,
			# width_shift_range=[-5, 5],
			# horizontal_flip=True,
			# shear_range = 3.5
			# zoom_range=[1.0,1.1],
			brightness_range=[0.7,1.1],
			# rotation_range=10,
			horizontal_flip=True,
			# shear_range = 3.5,
			# featurewise_center=True, featurewise_std_normalization=True,	zca_whitening=True
			)
			callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience = 4, min_delta=0, mode = 'min',restore_best_weights=True)
			cnn_model = tf.keras.models.load_model(f'D:\my_project\Awesome-Guys\Dataset\LT1\LT1_CNN_Model.pkl')
			#Huấn luyện mô hình CNN
			trainingDataSet, testingDataSet, trainingLabel, testingLabel = train_test_split(dataset['images'], dataset['classes'], test_size=0.3, random_state=42)
			print(trainingDataSet.shape)
			print(trainingLabel.shape)
			print(testingDataSet.shape)
			print(testingLabel.shape)
   
			history = cnn_model.fit(datagen.flow(trainingDataSet,trainingLabel, batch_size=32),validation_data=(testingDataSet,testingLabel),
								batch_size=16, epochs=100, verbose=1, callbacks = [callback])
			# history = cnn_model.fit( trainingDataSet,trainingLabel,validation_data=(testingDataSet,testingLabel),
			# 					batch_size=16, epochs=7, verbose=1, callbacks = [callback])
			# Testing callbacks = [callback], datagen.flow(dataset['images'], dataset['classes'], batch_size=32)
			print(cnn_model.metrics_names)
			# Đánh giá model với dữ liệu train
			print(cnn_model.evaluate(dataset['images'], dataset['classes'], verbose=1))
			# Đánh giá model với dữ liệu test set
			print(cnn_model.evaluate(dataset['images'], dataset['classes'], verbose=1))
			
			#Khởi tạo mô hình học chuyển tiếp
			tfl = TransferLearning_CNN_SVM(CNN_model=cnn_model)
			
			#Trích xuất thuộc tính từ ảnh
			feature_matrix = tfl.cnn_extract_feature(dataset['images'])
			# KFold = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)

			#Tạo và huấn luyện mô hình SVM
			

			clf = svm.SVC(kernel='rbf', C = 10, gamma=0.0001)
			# clf = svm.SVC(kernel='rbf')

			# KFold = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)

			# scores = cross_validate(clf, feature_matrix, dataset['classes'], cv=KFold, scoring='accuracy', return_estimator=True, return_train_score=True)

			# fit_times = scores['fit_time']
			# score_times = scores['score_time']
			# estimators = scores['estimator']
			# train_scores = scores['train_score'] * 100
			# test_scores = scores['test_score'] * 100

			# print('{:14s} {:20s} {:20s} {:15s} {:15s}'.format('', 'Training scores', 'Testing scores', 'Fit time', 'Score time'))

			# for i in range(5):
			# 	print('{:13s} {:10.2f}{:<} {:18.2f}{:<} {:17.2f} {:16.2f}'.format('Experiment ' + str(i + 1) + ':', train_scores[i], '%', test_scores[i], '%', fit_times[i], score_times[i]))

			# print('------------------------------------------------------------------------------------------')
			# print('{:>14s} {:9.2f}% {:18.2f}% {:17.2f} {:16.2f}'.format('Mean: ', np.mean(train_scores), np.mean(test_scores), np.mean(fit_times), np.mean(score_times)))
			# print('{:>14s} {:9.2f}% {:18.2f}% {:17.2f} {:16.2f}'.format('Highest: ', max(train_scores), max(test_scores), max(fit_times), max(score_times)))
			# print('{:>14s} {:9.2f}% {:18.2f}% {:17.2f} {:16.2f}'.format('Lowest: ', min(train_scores), min(test_scores), min(fit_times), min(score_times)))

			clf = svm.SVC(kernel = 'rbf', probability=True, C = 10, gamma=0.0001).fit(feature_matrix, dataset['classes'])

			#Test mô hình
			y_pred = clf.predict(feature_matrix)

			print("Accuracy: ", metrics.accuracy_score(dataset['classes'], y_pred))

			print("Precision: ", metrics.precision_score(dataset['classes'], y_pred, average=None))
			print("Recall: ", metrics.recall_score(dataset['classes'], y_pred, average=None))

			#Lưu các mô hình
			cnn_model.save(f'{directory}/{classes}_CNN_Model.pkl')
			pickle.dump(clf, open(f'{directory}/{classes}_SVM_Model.pkl', 'wb'))

			return Response({}, status=status.HTTP_200_OK)
		except Exception as errors:
			print(errors)
			return Response(str(errors), status=status.HTTP_400_BAD_REQUEST)