from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Subnet)
admin.site.register(models.Host)

