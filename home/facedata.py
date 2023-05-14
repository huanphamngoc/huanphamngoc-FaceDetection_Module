import os
import numpy as np
import pickle
from PIL import Image
from django.conf import settings

from faceregister.models import AnhDangKy, ChiTietLopHoc
from FaceRecognitionDemo.firebase import Firebase


class DatasetManagement():
    '''Lớp cung cấp các phương thức thao tác với face dataset'''
    def __init__(self, directory):
        """Hàm khởi tạo
        - directory: đường dẫn đến thư mục chứa dataset
        """
        self.directory = directory

    def create_face_dataset(self):
        """Hàm tạo và lưu dataset xuống đĩa"""
        classes = f'LT1'
        #Kiểm tra đường dẫn, nếu không tồn tại thì tạo mới
        if(os.path.exists(self.directory) == False):
            os.makedirs(self.directory)

        #Khỏi tạo Firebase
        firebase = Firebase(settings.FIREBASE_CONFIGURE)

        #Khởi tạo các danh sách lưu thông tin cần thiết
        # dataset = pickle.load(open('D:\my_project\Awesome-Guys\Dataset\LT1\LT1_ImageDataset.pkl','rb'))
        
        # print(dataset.keys())
        # images = dataset['images']
        # labels = dataset['classes']
        # class_names = dataset['student_names']
        
        # student_images_list = list(dataset['images'])
        # student_labels_list = list(dataset['classes'])
        # student_names_list = list(dataset['student_names'])
        # student_ids_list = list(dataset['student_ids'])
        
        student_images_list = list()
        student_labels_list = list()
        student_names_list = list()
        student_ids_list = list()   
        #Lấy tất cả sinh viên có trong lớp 'LT1'
        classes_details = ChiTietLopHoc.objects.filter(lop_hoc__ma_lop='LT1')
        print(classes_details)

        #Duyệt từng sinh viên trong lớp 'LT1'
        for index, detail in enumerate(classes_details):
            #Lấy thông tin về ảnh của sinh viên
            registration_images = AnhDangKy.objects.filter(
                sinh_vien=detail.sinh_vien
            )
            #Lưu tên và id của sinh viên
            student_names_list.append(detail.sinh_vien.ho_ten)
            student_ids_list.append(detail.sinh_vien.masv)

            #Duyệt từng ảnh đã đăng ký của sinh viên
            i = 0
            for image_infor in registration_images:
                #Đọc ảnh từ Firebase
                image = firebase.read_an_image_from_storage(image_infor.duong_dan_anh)
                # im = Image.fromarray(image[:120, 30:110])
                # im.save( "./image/image"+str(i) +".jpeg")
                # i+=1
                
                #Lưu ảnh và nhãn của sinh viên
                student_images_list.append(image[:120, 30:110])
                student_labels_list.append(index)
        #Tạo dataset theo các thông có được
        dataset = {'images': np.array(student_images_list),
                'classes': np.array(student_labels_list),
                'student_names': student_names_list,
                'student_ids': student_ids_list}
        
        print(dataset.keys())
        images = dataset['images']
        labels = dataset['classes']
        class_names = dataset['student_names']
        print(images.shape)
        print(labels.shape)
        print(class_names)
        print(labels)
        #Ghi dữ liệu xuống đĩa
        pickle.dump(dataset, open(f'{self.directory}/{classes}_ImageDataset.pkl', 'wb'))
        pickle.dump(student_names_list, open(f'{self.directory}/{classes}_StudentNames.pkl', 'wb'))
        pickle.dump(student_ids_list, open(f'{self.directory}/{classes}_StudentIDs.pkl', 'wb'))

        #Trả về tập dữ liệu
        return dataset