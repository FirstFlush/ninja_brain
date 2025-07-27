from django.db import models


class EntityPrediction(models.Model):
    
    sms_inquiry_id = models.IntegerField()
    model_version = models.CharField(max_length=16)
    extracted_entities = models.JSONField()
    # resolved_location = models.CharField(max_length=256)
    response_time_ms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)