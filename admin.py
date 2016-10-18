from django.contrib import admin
from . import models

admin.site.register(models.Subnet)
admin.site.register(models.Host)

