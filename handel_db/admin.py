from django.contrib import admin
from .models import Database, Artifact, Collection
# Register your models here.

admin.site.register(Database)
admin.site.register(Artifact)
admin.site.register(Collection)