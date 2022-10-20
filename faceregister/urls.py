from django.urls import path

from .views import TakingFrontalFace, FaceRegisterAPIView,SaveFrontalFace,FaceRegisterImageAPIView
app_name = 'faceregister'

urlpatterns = [
    path("", FaceRegisterAPIView.as_view(), name="face-register"),
    path("registerImage/", FaceRegisterImageAPIView.as_view(), name="image-register"),
    # path('takingfrontalface/<int:masv>/', TakingFrontalFace.as_view(), name="taking-frontal-face"),
    path('takingfrontalface/', TakingFrontalFace.as_view(), name="taking-frontal-face"),
    path('savefrontalface/', SaveFrontalFace.as_view(), name="save-frontal-face")
]
