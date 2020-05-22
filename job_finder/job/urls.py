from django.urls import path,include
from job import views

app_name = 'job'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    
]