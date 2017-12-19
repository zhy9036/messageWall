from django.db import models
from django.utils import timezone
# Create your models here.

class Message(models.Model):
    content = models.CharField(max_length=2000)
    create_date = models.DateTimeField(default=timezone.now)