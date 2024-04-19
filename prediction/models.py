from django.db import models

class PredictionImage(models.Model):
    before_predict = models.ImageField(upload_to='img_before/')
    after_predict = models.ImageField(upload_to='img_after/')
