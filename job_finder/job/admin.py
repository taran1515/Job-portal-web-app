from django.contrib import admin
from job.models import User, UserProfileInfo,Company
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(Company)
