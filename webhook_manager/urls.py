from django.urls import path
from . import views

urlpatterns = [
    path('line_webhook/', views.line_webhook, name='line_webhook'),
    path('get_user_id/<str:user_id>/<str:reply_token>/', views.get_user_id, name='get_user_id'),
]