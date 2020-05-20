from django.shortcuts import render
from .models import UserProfileInfo,Company
from job.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    print(request.user.id)
    if(request.user.id):
        curr_user = UserProfileInfo.objects.get(id=request.user.id-1)
    else:
        curr_user = []
    return render(request,'job/index.html',{'current_user':curr_user})

def company(request):
    curr_user = UserProfileInfo.objects.get(id=request.user.id-1)
    # print(curr_user.company.id)
    company = Company.objects.get(id=curr_user.company.id)
    # print(company.company_name)
    return render(request,'job/company.html',{'company':company})
    
@login_required
def special(request):
    return HttpResponse("You are logged in !")
    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'job/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
                           
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return render(request,'job/login_failed.html',{})
    else:
        return render(request, 'job/login.html', {})