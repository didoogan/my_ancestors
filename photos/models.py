from django.db import models

from ancestors.models import Ancestor


class Photo(models.Model):
    photo = models.ImageField()
    uploaded = models.DateField(auto_now_add=True)
    ancestor = models.ForeignKey(Ancestor)
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        return self.ancestor.user.email
