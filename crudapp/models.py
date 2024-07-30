from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User1(models.Model):
    uname = models.CharField(max_length=100)
    uaddress = models.CharField(max_length=100)

    uphone = models.CharField(max_length=100)

    class Meta:
        db_table = "users"


class Contact1(models.Model):
    uname = models.CharField(max_length=100)
    uemail = models.CharField(max_length=100)
    uphone = models.CharField(max_length=100)
    uservices = models.CharField(max_length=100)

    class Meta:
        db_table = "userlist"


class CustomUser(AbstractUser):
    previous_login = models.DateTimeField(null=True, blank=True,default=None)

    def update_last_login(self):

        lastLogin = self.previous_login
        self.previous_login = timezone.now()
        self.save()
        return lastLogin