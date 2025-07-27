from django.db import models


class EntityPrediction(models.Model):
    
    sms_id = models.IntegerField()
    model_version = models.CharField(max_length=16)
    extracted_entities = models.JSONField()
    response_time_ms = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)