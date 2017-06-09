from django.contrib import admin
from .models import Ancestor


class AncestorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Ancestor, AncestorAdmin)
