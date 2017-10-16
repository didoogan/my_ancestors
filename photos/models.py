from django.db import models

from ancestors.models import Ancestor


class Photo(models.Model):
    photo = models.ImageField()
    uploaded = models.DateField(auto_now_add=True)
    ancestor = models.ForeignKey(Ancestor, related_name='photos')
    is_avatar = models.BooleanField(default=False)

    def __str__(self):
        return self.ancestor.first_name

    class Meta:
        unique_together = ('ancestor', 'is_avatar')
