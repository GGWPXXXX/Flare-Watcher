from django.urls import path
from . import views

urlpatterns = [
    path('line_webhook/', views.line_webhook, name='line_webhook'),
    path('get_last_user_id/', views.get_last_user_id, name='get_last_user_id'),
]