from django.db import models
from django.contrib.auth.models import User

class PendingAuth(models.Model):
    token = models.CharField(max_length=32)
    url = models.CharField(max_length=2000)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %s" % (self.token, self.datetime)

class PendingLogin(models.Model):
    token = models.CharField(max_length=32)
    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=128)

    def __unicode__(self):
        return "%s, %s, %s" % (self.username, self.token, self.datetime)

class SQRLUser(models.Model):
    user = models.OneToOneField(User)

    identity_key = models.TextField()

    def get_username(self):
        return self.user.get_username()

    def __unicode__(self):
        return self.user.username



