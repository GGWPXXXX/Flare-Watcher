from django.db import models


class BeforePredictionImage(models.Model):
    before_predict = models.ImageField(upload_to='img_before/')
    
class AfterPredictionImage(models.Model):  
    after_predict = models.ImageField(upload_to='img_after/')
    