from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.
'''
class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.CharField(max_length=2000)
    create_date = models.DateTimeField(default=timezone.now)
'''