from django.conf import settings
from django.db import models


class Ancestor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True,
                                null=True)
    parents = models.ManyToManyField("self", blank=True, null=True)
    birth = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    bio = models.TextField()
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    third_name = models.CharField(max_length=20, null=True, blank=True)

    def get_full_name(self):
        return '{} {} {}'.format(self.first_name, self.last_name,
                                 self.third_name)

    def __str__(self):
        return self.get_full_name()
