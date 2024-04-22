from django.db import models


class BeforePredictionImage(models.Model):
    before_predict = models.ImageField(upload_to='img_before/')
    
class AfterPredictionImage(models.Model):  
    after_predict = models.ImageField(upload_to='img_after/')
    
# class Prediction(models.Model):
#     user_id = models.CharField(max_length=50)
#     Humidity = models.FloatField()
#     TVOC = models.FloatField()
#     eCO2 = models.FloatField()
#     Pressure = models.FloatField()
#     flame_sensor = models.BooleanField()
#     img = models.ImageField(upload_to='img/')
#     prediction = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user_id
    
# Path: prediction/urls.py
