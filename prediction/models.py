from django.db import models

class Prediction(models.Model):
    user_id = models.CharField(max_length=100)
    prediction = models.CharField(max_length=100)
    Humidity = models.FloatField()
    TVOC = models.FloatField()
    Pressure = models.FloatField()
    eCO2 = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

