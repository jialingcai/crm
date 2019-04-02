from django.contrib import admin
from crm import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.Department)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
