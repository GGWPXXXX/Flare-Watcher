from django.db import models

class LineWebhook(models.Model):
    event_type = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
