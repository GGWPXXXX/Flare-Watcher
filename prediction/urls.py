from django.urls import path
from . import views


app_name="webhook_manager"
urlpatterns = [
    path('sensor_prediction/', views.sensor_prediction_view, name='sensor_prediction_view'),
]