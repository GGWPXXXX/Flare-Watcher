from django.urls import path
from . import views

urlpatterns = [
    path('line_webhook/', views.line_webhook, name='line_webhook'),
    path("test_post/", views.test_post, name="test_post"),
    path('get_line_user_id/', views.get_line_user_id, name='get_line_user_id'),
    
]