from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.


class Message(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    create_date = models.DateTimeField(default=timezone.now)

    @property
    def get_username(self):
        return User.objects.get(pk=self.user_id).username

    def __str__(self):
        return str(self.get_username()) + ' created at: ' + str(self.create_date)


