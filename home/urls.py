from django.urls import path

from .views import HomeAPIView, ModelsTrainingAPI

app_name = 'home'

urlpatterns = [
	path('', HomeAPIView.as_view(), name='home'),
	path('training/', ModelsTrainingAPI.as_view(), name="models-training")
]