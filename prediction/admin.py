from django.contrib import admin
from . import models

admin.site.register(models.BeforePredictionImage)
admin.site.register(models.OriginalSizePredictionImage)
admin.site.register(models.CompressedPredictionImage)
