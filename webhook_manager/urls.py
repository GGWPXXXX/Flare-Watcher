from django.urls import path
from . import views

app_name = 'webhook_manager'
urlpatterns = [
    path('line_webhook/', views.line_webhook, name='line_webhook'),
]