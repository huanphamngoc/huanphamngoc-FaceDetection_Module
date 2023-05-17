
from django.conf import settings
import base64
from django.shortcuts import render
from django.db import transaction

from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SinhVienSerializer, ChiTietLopHocSerializer, AnhDangKySerializer

from .exceptions import SinhVienException, ChiTietLopHocException, AnhDangKyException

from FaceRecognitionDemo.firebase import Firebase
import pickle
import numpy as np
import base64
import cv2
from django.conf import settings
from django.shortcuts import render
import io
from PIL import Image
from django.db.models import Count
from .models import ChiTietLopHoc, SinhVien, AnhDangKy
import pickle
# Create your views here.
class FaceRegisterAPIView(APIView):
    template_name = 'faceregister/index.html'
    
    def get(self, request):
        return render(request, self.template_name, {})
    
    def post(self, request):
        pass
class FaceRegisterImageAPIView(APIView):
    template_name = 'faceregister/faceregister.html'
    
    def get(self, request):
        return render(request, self.template_name, {})
    
    def post(self, request):
        pass


class TakingFrontalFace(APIView):
    template_name = 'faceregister/index.html'

    successful_notification = {
        'message': 'Thêm sinh viên thành công'
    }

    def get(self, request):
        print("Đây là :", request.query_params['masv'])
        # FaceDetection.create_dataset(request.query_params['masv'])
        return render(request, self.template_name, {})

    def post(self, request):
        masv = request.data["masv"]
        sinhvien_serializer = SinhVienSerializer(data=request.data)
        print( request.data)
        try:
            with transaction.atomic():
                
                if sinhvien_serializer.is_valid():
                    sinhvien_serializer.save()
                    
                    chitietlophoc_data = {
                        'sinh_vien': masv,
                        'lop_hoc': 'LT1'
                    }
                    chitietlophoc_serializer = ChiTietLopHocSerializer(data = chitietlophoc_data)
                    if chitietlophoc_serializer.is_valid():
                        chitietlophoc_serializer.save()
                        return Response(sinhvien_serializer.data, status = status.HTTP_201_CREATED)
                    else:
                        raise ChiTietLopHocException(chitietlophoc_serializer.errors)
                    
                else:
                    raise SinhVienException(sinhvien_serializer.errors)
        except (SinhVienException, ChiTietLopHocException) as errors:
            transaction.rollback()
            return Response(str(errors), status=status.HTTP_400_BAD_REQUEST)
# Luu du lieu anh dang ky
class SaveFrontalFace(APIView):
    def post(self, request):
        directory = f'Dataset/LT1'
        classes = f'LT1'
        duong_dan_anh = request.data['duong_dan_anh']
        masv = request.data['masv']
        folder_path = f'demo_faceregister/{masv}'
        firebase = Firebase(settings.FIREBASE_CONFIGURE)
        face_dataset = dict()
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
        print(labels)
        images1 = images.tolist()
        labels = labels.tolist()
        nhan = Student_ids.index(masv)
        # ChiTietLopHoc.objects.values('id').count()-1
        # print(a.count())
        print(nhan)
        print((labels[10]))
        print(type(nhan))
        masv1 = masv
        Student_ids.append(masv)
        class_names.append(SinhVien.objects.get(masv = masv1).ho_ten)
        # b = SinhVien.objects.get(masv = masv1).ho_ten
        # print(b)  
        
        templabels = []      
        tempimages = []
        for i in range(len(labels)):
            if(labels[i] != nhan):
                templabels.append(labels[i])
                tempimages.append(images[i])
        images = tempimages
        labels = templabels
        print(labels)
        try:
            with transaction.atomic():
                for index, link in enumerate(duong_dan_anh):
                    # timedt = datetime.datetime.now()
                    # print(f'{masv}_{timedt}.jpg')
                    duong_dan_anh_temp = (np.array(Image.open(io.BytesIO((base64.b64decode(link))))))[:120, 30:110]
                    images.append(duong_dan_anh_temp)
                    labels.append(nhan)
                    # duong_dan_anh2 = ((Image.open(io.BytesIO((base64.b64decode(link))))))

                    # duong_dan_anh2.save("/save/image"+str(index)+".jpg")
                    face_dataset[f'{masv}_{index}.jpg'] = base64.b64decode(link)
                    # image = (np.array(Image.open(io.BytesIO((base64.b64decode(link))))))[:, 20:100]
                    # face_dataset[f'{masv}_{index}.jpg'] = cv2.imencode('.jpg', cv2.cvtColor(image , cv2.COLOR_RGB2BGR))[1].tobytes()
                    # face_dataset[f'{masv}_{timedt}.jpg'] = cv2.imencode('.jpg', cv2.cvtColor(image , cv2.COLOR_RGB2BGR))[1].tobytes()
                image_links = firebase.upload_images_to_storage(folder_path, face_dataset, masv)
                anhdangky_serializer = AnhDangKySerializer(data=image_links, many=True)
                student_images_list = images
                student_labels_list = labels
                student_ids_list = Student_ids
                student_names_list = class_names
                dataset = {'images': np.array(student_images_list),
                'classes': np.array(student_labels_list),
                'student_names': student_names_list,
                'student_ids': student_ids_list}
                images = dataset['images']
                labels = dataset['classes']
                class_names = dataset['student_names']
                Student_ids = dataset['student_ids']
                print(images.shape)
                print(labels.shape)
                # print(images)
                print(class_names)
                print(labels)
                # print(dataset)
        #Ghi dữ liệu xuống đĩa
                pickle.dump(dataset, open(f'{directory}/{classes}_ImageDataset.pkl', 'wb'))
                pickle.dump(student_names_list, open(f'{directory}/{classes}_StudentNames.pkl', 'wb'))
                pickle.dump(student_ids_list, open(f'{directory}/{classes}_StudentIDs.pkl', 'wb'))
                if anhdangky_serializer.is_valid():
                    anh = AnhDangKy.objects.filter(sinh_vien_id = masv);
                    # anh.delete()
                    # anhdangky_serializer.save()
                    return Response(anhdangky_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise AnhDangKyException(anhdangky_serializer.errors, stautus = status.HTTP_400_BAD_REQUEST)
        except:
            transaction.rollback()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

        
        
# class SaveFrontalFace(APIView):
#     template_name = 'faceregister/index.html'
# # class SaveFrontalFace(APIView):
# #     template_name = 'faceregister/index.html'

#     successful_notification = {
#         'message': 'Thêm sinh viên thành công'
#     }
# #     successful_notification = {
# #         'message': 'Thêm sinh viên thành công'
# #     }

#     def get(self, request):
#         print("Đây là :", request.query_params['masv'])
#         # FaceDetection.create_dataset(request.query_params['masv'])
#         return render(request, self.template_name, {})
# #     def get(self, request):
# #         print("Đây là :", request.query_params['masv'])
# #         # FaceDetection.create_dataset(request.query_params['masv'])
# #         return render(request, self.template_name, {})

# #     def post(self, request):
# #         image_links = request.data
# #         try:
# #             with transaction.atomic():
# #                 anhdangky_serializer = AnhDangKySerializer(data=image_links, many=True)
# #                 if anhdangky_serializer.is_valid():
# #                     anhdangky_serializer.save()
# #                     return Response(anhdangky_serializer.data, status=status.HTTP_201_CREATED)
# #                 else:
# #                     raise AnhDangKyException(anhdangky_serializer.errors)
# #         except (AnhDangKyException) as errors:
# #             transaction.rollback()
# #             return Response(str(errors), status=status.HTTP_400_BAD_REQUEST)