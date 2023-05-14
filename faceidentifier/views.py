import pickle
import numpy as np
import base64
import cv2
from django.conf import settings
from django.shortcuts import render
import io
from PIL import Image
# import keras
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from FaceRecognitionDemo.firebase import Firebase
from home.transfer_learning import TransferLearning_CNN_SVM
import datetime
from .serializers import DinhDanhKhuonMatSerializer, DinhDanhThuCongSerializer
from .exceptions import DinhDanhKhuonMatException
from faceregister.models import ChiTietLopHoc
#Tạo biến lưu student id
last_student_id = 'unknown'

#Tạo biến lưu sinh viên
recognized_student = None

class FaceAPIView(APIView):
    template_name = 'faceidentifier/details.html'
    
    def get(self, request):
        return render(request, self.template_name, {})
class FaceidentifiterAPI(APIView):
    @staticmethod
    def modeltfl():
        directory = f'Dataset/LT1'
        folder_path = f'identification Images/LT1'
        classes = f'LT1'
        tfl = TransferLearning_CNN_SVM(
            CNN_path=f'{directory}/{classes}_CNN_Model.pkl',
            SVM_path=f'{directory}/{classes}_SVM_Model.pkl'
        )
        return tfl
    
    def post(self,request):
        directory = f'Dataset/LT1'
        folder_path = f'identification Images/LT1'
        classes = f'LT1'
        tfl = FaceidentifiterAPI.modeltfl()
        student_names_list = pickle.load(open(f'{directory}/{classes}_StudentNames.pkl', 'rb'))
        student_ID_list = pickle.load(open(f'{directory}/{classes}_StudentIDs.pkl', 'rb'))
        image =  (np.array(Image.open(io.BytesIO((base64.b64decode(request.data))))))[:120, 30:110]
        # image = cv2.cvtColor(image , cv2.COLOR_RGB2BGR)
        feature_vector = tfl.cnn_extract_feature((image.reshape(1, 120, 80, 3)))
        # cnn_model1 = keras.models.load_model(f'D:\my_project\Awesome-Guys\Dataset\LT1\LT1_CNN_Model.pkl')
        # perc = cnn_model1.predict(image.reshape(1, 120, 80, 3))
        # prob = max(perc[0])*100;
        prob = max(tfl.SVM.predict_proba(feature_vector)[0]);
        prob1 = tfl.SVM.predict(feature_vector)[0]
        # class_of_vector = np.argmax(prob1[0])
        # prob = prob1[0][class_of_vector]
        print(prob1)
        student_name = student_names_list[prob1]
        student_id = student_ID_list[prob1]
        timedt = datetime.datetime.now()
        face = dict()
        image = cv2.cvtColor(image , cv2.COLOR_RGB2BGR)
        face[str(timedt)+student_id] = cv2.imencode('.jpg', image )[1].tobytes()
        firebase = Firebase(settings.FIREBASE_CONFIGURE)
        image_links = firebase.upload_images_to_storage(folder_path, face, 'LT1')[0]
        print(prob)
        print(image_links)
        print(student_name)
        if prob > 0.1 :
            # chitiet = 
            # print((ChiTietLopHoc.objects.get(sinh_vien = student_id, lop_hoc = 'LT1')).id)
            data_dinhdankhuonmat = {
                'duong_dan_anh':image_links['duong_dan_anh'],
                'thoi_gian': timedt,
                'status' : '1',
                'chitietlophoc_id':1,
                'chitietlophoc':'1'
                }
            # print(data_dinhdankhuonmat)
            dinhdanhkhuonmat_serializer = DinhDanhKhuonMatSerializer(data = data_dinhdankhuonmat)
            if dinhdanhkhuonmat_serializer.is_valid():
                dinhdanhkhuonmat_serializer.save()
                return Response(student_name,status=status.HTTP_201_CREATED)
            else:
                raise DinhDanhKhuonMatException(dinhdanhkhuonmat_serializer.data)
        else:
            data_dinhdankhuonmat = {
                'duong_dan_anh':image_links['duong_dan_anh'],
                'thoi_gian': timedt,
                'status' : '0',
                'chitietlophoc_id':(ChiTietLopHoc.objects.get(sinh_vien = student_id, lop_hoc = 'LT1')).id,
                'chitietlophoc':'1'
                }
            dinhdanhkhuonmat_serializer = DinhDanhKhuonMatSerializer(data = data_dinhdankhuonmat)
            if dinhdanhkhuonmat_serializer.is_valid():
                dinhdanhkhuonmat_serializer.save()
                return Response(prob,status=status.HTTP_400_BAD_REQUEST)
            else:
                raise DinhDanhKhuonMatException(prob, dinhdanhkhuonmat_serializer.data)
class ManualIDAPI(APIView):
    def post(self,request):
        print(request.data)
        data_dinhdanhthucong = {
            'thoi_gian':datetime.datetime.now(),
            'chitietlophoc_id':(ChiTietLopHoc.objects.get(sinh_vien = request.data, lop_hoc = 'LT1')).id,
            'chitietlophoc':'1'
            }
        dinhdanhthucong_serializer = DinhDanhThuCongSerializer(data = data_dinhdanhthucong)
        if dinhdanhthucong_serializer.is_valid():
            dinhdanhthucong_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
                
            