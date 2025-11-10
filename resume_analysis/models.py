from django.db import models
from django.contrib.auth.models import User
import uuid

class ResumeAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_text = models.TextField()
    job_description = models.TextField()
    ats_score = models.FloatField(null=True, blank=True)
    matched_keywords = models.JSONField(default=list, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_id = models.UUIDField(null=True, blank=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    


