from django.db import models

class UnclaimedSession(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, %s" % (self.id, self.datetime)

