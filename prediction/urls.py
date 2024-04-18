from django.urls import path
from . import views


app_name="prediction"
urlpatterns = [
    path('sensor_prediction/', views.sensor_prediction_view, name='sensor_prediction_view'),
    path('image_prediction/', views.image_prediction_view, name='image_prediction_view'),
]