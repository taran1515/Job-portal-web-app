from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='company',blank=True)
    address = models.CharField(max_length=100)
    

    def __str__(self):
        return self.company_name


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE),
    profile_pic = models.ImageField(upload_to='job/',blank=True)
    job_role = models.CharField(max_length=100)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    visited = models.BooleanField(default=False)
    visited_company_page = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

