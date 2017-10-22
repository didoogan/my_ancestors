from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Ancestor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True,
                                null=True)
    parents = models.ManyToManyField("self", blank=True,
                                     related_name="children",
                                     symmetrical=False)
    ancestors = models.ManyToManyField("self", blank=True,
                                       related_name='ancestor')
    birth = models.DateField(null=True, blank=True)
    death = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    third_name = models.CharField(max_length=120, blank=True)
    gender = models.NullBooleanField()
    abstract = models.BooleanField(default=False)

    class Meta:
        unique_together = ('first_name', 'last_name', 'birth')

    @property
    def childrens(self):
        return self.children.all().exclude(id=self.id)

    @property
    def siblings(self):
        try:
            return self.parents.all()[0].children.exclude(id=self.id)
        except IndexError:
            return []

    def get_full_name(self):
        return '<Ancestor> {} {} {}'.format(self.last_name, self.first_name,
                                 self.third_name)

    # def save(self, *args, **kwargs):
    #     ancestor = super(Ancestor, self).save(*args, **kwargs)
    #     for person in ancestor.ancestors.all():
    #         person.ancestors.add(ancestor)

    def __str__(self):
        if self.abstract:
            return '<Abstract Ancestor>'
        return self.get_full_name()
