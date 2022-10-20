from django.urls import path

from .views import FaceidentifiterAPI, FaceAPIView,ManualIDAPI

app_name = 'faceidentifier'

urlpatterns = [
	path('', FaceAPIView.as_view(), name='scanner'),
	path('faceidentifier/', FaceidentifiterAPI.as_view()),
	path('Manual/', ManualIDAPI.as_view()),
]