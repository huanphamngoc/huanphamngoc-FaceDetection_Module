from cgitb import text
import os
from unittest import result
import cv2
import numpy as np
import pickle
from typing import Tuple

import imutils
from imutils.video import VideoStream
from imutils import face_utils

from PIL import Image, ImageDraw, ImageFont

from django.conf import settings

from FaceRecognitionDemo.firebase import Firebase
from home.transfer_learning import TransferLearning_CNN_SVM

FACE_CASCADE = cv2.CascadeClassifier(os.path.join(
    settings.BASE_DIR,
    'opencv_haarcascade_model\haarcascade_frontalface_default.xml'
))

class WebCam():
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        if not self.video.isOpened():
            raise IOError("Cannot open webcam")

        ret, image = self.video.read()
        if not ret:
            return("Error: failed to capture image")

        return image

def generate_frame(camera: WebCam):
    print("[INFO] Initializing Video stream")
    while True:
        frame = FaceID().draw_around_faces(camera.get_frame())
        yield frame


class FaceID():

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_faces = FACE_CASCADE.detectMultiScale(
            gray, scaleFactor=1.05, minNeighbors=10, minSize=(150, 150))
        return detected_faces

    def draw_around_faces(self, frame:np.ndarray, detected_faces:np.ndarray):
        for (x, y, w, h) in detected_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame

    def crop_faces(self, frame:np.ndarray, detected_faces:np.ndarray):
        x, y, w, h = detected_faces[0]

        # Crop frontal face
        frontal_face = frame[y:y+h, x:x + w]

        # Resize to a small resolution without changing ratio
        frontal_face = cv2.resize(frontal_face, (120, 120),
                                    interpolation=cv2.INTER_LINEAR_EXACT)

        cropped_face = frontal_face[:, 20:100]
        return cropped_face

    def cv2_img_add_unicode_text(self, img, text, left_corner: Tuple[int, int],
                            text_rgb_color=(255, 0, 0), text_size=24, font='arial.ttf', **option):
        pil_img = img
        if isinstance(pil_img, np.ndarray):
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        font_text = ImageFont.truetype(font=font, size=text_size, encoding=option.get('encoding', 'utf-8'))
        draw.text(left_corner, text, text_rgb_color, font=font_text)
        cv2_img = cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)
        return cv2_img

    def create_dataset(self, masv, max_samples:int, camera:WebCam):
        face_dataset = dict()
        
        sample_num = 0
        while(True):
            frame = camera.get_frame()
            detected_faces = self.detect_face(frame)

            if not isinstance(detected_faces, np.ndarray):
                cv2.putText(frame, "Face not found", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if detected_faces.shape[0] > 1:
                    cv2.putText(frame, "Only one person in the camera", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    sample_num = sample_num+1
                    cropped_face = self.crop_faces(frame, detected_faces)
                    
                    byte_image = cv2.imencode('.jpg', cropped_face)[1].tobytes()
                    face_dataset[f'{masv}_{sample_num}.jpg'] = byte_image
                    
                    cv2.putText(frame, str(sample_num), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                
            frame = self.draw_around_faces(frame, detected_faces)
            
            cv2.imshow("Taking picture", frame)

            key = cv2.waitKey(100) & 0xff
            if key==27 or sample_num >= max_samples:
                del camera
                cv2.destroyAllWindows()
                break
        return face_dataset

    def recognize_face(self, class_id, camera:WebCam):
        directory = f'Dataset/{class_id}'
        student_names_list = pickle.load(open(f'{directory}/{class_id}_StudentNames.pkl', 'rb'))
        student_ID_list = pickle.load(open(f'{directory}/{class_id}_StudentIDs.pkl', 'rb'))
        
        tfl = TransferLearning_CNN_SVM(
            CNN_path=f'{directory}/{class_id}_CNN_Model.pkl',
            SVM_path=f'{directory}/{class_id}_SVM_Model.pkl'
        )

        while(True):
            frame = camera.get_frame()
            detected_faces = self.detect_face(frame)

            if not isinstance(detected_faces, np.ndarray):
                cv2.putText(frame, "Face not found", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                if detected_faces.shape[0] > 1:
                    cv2.putText(frame, "Only one person in the camera", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cropped_face = self.crop_faces(frame, detected_faces)
                    feature_vector = tfl.cnn_extract_feature(cropped_face.reshape(1, 120, 80, 3))
                    prob = tfl.SVM.predict_proba(feature_vector)
                    class_of_vector = np.argmax(prob[0])
                    prob = prob[0][class_of_vector]
                    student_name = student_names_list[class_of_vector]
                    student_id = student_ID_list[class_of_vector]

                    x, y, w, h = detected_faces[0]

                    cv2.rectangle(frame, (x, y + h + 35), (x + w, y + h), (0, 0, 255), cv2.FILLED)
                    
                    if prob >= 0.5:
                        result_text = f'{student_name}|{round(prob, 2)}'
                    else:
                        result_text = "Unknown"

                    frame = self.cv2_img_add_unicode_text(
                        frame,
                        result_text, 
                        left_corner=(x, y + h + 5), 
                        text_rgb_color=(255, 255, 255),
                        text_size=22,
                    )

                    yield prob, student_id, student_name

            frame = self.draw_around_faces(frame, detected_faces)
            
            cv2.imshow("Taking picture", frame)
            
            key = cv2.waitKey(1) & 0xff
            if key==27:
                break

