from django.db import models
from .enums import MLModelEnum


class MLModel(models.Model):
    
    name = models.CharField(max_length=256, unique=True, choices=MLModelEnum.choices)
    version = models.CharField(max_length=24)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'version'], name='unique_model_version')
        ]

class EntityPrediction(models.Model):
    
    sms_id = models.IntegerField()
    ml_model = models.ForeignKey(to=MLModel, on_delete=models.CASCADE, related_name="predictions")
    extracted_entities = models.JSONField()
    response_time_ms = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)