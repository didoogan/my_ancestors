from django.db import models

from ancestors.models import Ancestor


class Photo(models.Model):
    photo = models.ImageField()
    uploaded = models.DateField(auto_now_add=True)
    ancestor = models.ForeignKey(Ancestor, related_name='photos')

    def __str__(self):
        return self.ancestor.first_name
