import imp
import pickle

import keras
from keras.models import Model, Sequential
from sklearn import svm


class TransferLearning_CNN_SVM():
    ''' Lớp mô hình học chuyển tiếp CNN -> SVM
    '''
    def __init__(self, CNN_model:Sequential = None, CNN_path:str = None, SVM_classifier:svm.SVC = None, SVM_path:str = None):
        """Phương thức khởi tạo mô hình học chuyển tiếp CNN -> SVM
        - CNN_model: mô hình CNN
        - CNN_path: đường dẫn đến mô hình CNN
        - SVM_classifier: mô hình SVM
        - SVM_path: đường dẫn đến mô hình SVM
        """

        #Kiểm tra xem CNN model Object có được truyền vào không?
        if isinstance(CNN_model, Sequential):
            self.CNN = CNN_model
        else: #Nếu không thì load model theo đường dẫn
            self.CNN = keras.models.load_model(CNN_path)

        #Kiểm trả xem thông tin mô hình SVM có được cung cấp không?
        if SVM_classifier is not None or SVM_path is not None:
            if isinstance(SVM_classifier, svm.SVC): #Nếu SVM model Object được cung cấp
                self.SVM = SVM_classifier
            else: #Không thì khởi tạo theo đường dẫn
                self.SVM = pickle.load(open(SVM_path, 'rb'))
        else: #Nếu không thì khởi tạo None
            self.SVM = None

        #Tạo feature_extractor từ mô hình CNN loại bỏ lớp cuối
        self.feature_extractor = Model(inputs=self.CNN.inputs, outputs=self.CNN.layers[-3].output)

    def cnn_extract_feature(self, images):
        """Hàm trích chọn thuộc tính từ ảnh
        - images: tập ảnh khuôn mặt
        """
        feature_matrix = self.feature_extractor.predict(images)

        return feature_matrix