from django.db import models

class Prediction(models.Model):
    user_id = models.CharField(max_length=100)
    Humidity = models.FloatField()
    TVOC = models.FloatField()
    Pressure = models.FloatField()
    eCO2 = models.FloatField()
    image_prediction = models.BooleanField()
    sensor_prediction = models.BooleanField()
    flame_detected = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

