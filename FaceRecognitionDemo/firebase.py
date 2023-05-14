import io
import urllib
from PIL import Image
import pyrebase
import numpy as np

class Firebase():
    def __init__(self, firebase_config):
        self.firebase_config = firebase_config
        self.firebase = pyrebase.initialize_app(firebase_config)
        self.storage = self.firebase.storage()

    def upload_images_to_storage(self, folder_path:str, images:dict, masv):
        image_links = list()

        for key, image in images.items():
            directory = folder_path + '/' + key
            self.storage.child(directory).put(image)
            url = self.storage.child(directory).get_url(None)
            image_links.append({
                'duong_dan_anh': url, 
                'sinh_vien': masv
            })
        return image_links

    def upload_file_to_storage(self, directory, file):
        print(directory)
        self.storage.child(directory).put(file)
    


    def read_an_image_from_storage(self, url):
        file = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(file)) #RGB
        
        return np.array(image)

