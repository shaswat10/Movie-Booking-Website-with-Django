from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.MovieMaster)
admin.site.register(models.AdminSide)
admin.site.register(models.SetMovie)