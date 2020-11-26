from django.contrib import admin

from accounts.models import CustomUser, Dates

admin.site.register(CustomUser)
admin.site.register(Dates)
# Register your models here.
