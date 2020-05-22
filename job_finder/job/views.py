from django.shortcuts import render
from .models import UserProfileInfo,Company
from django.contrib.auth.models import User
from job.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    print(request.user.id)
    if(request.user.id is not None):
        print(request.user.username)
        user_id = User.objects.get(username=request.user.username)
        print(user_id.id)
        curr_user = UserProfileInfo.objects.get(id=user_id.id-1)
        (curr_user.visited_company_page) = False
        curr_user.save()
    else:
        curr_user = []
    return render(request,'job/index.html',{'current_user':curr_user})

def company(request):
    # print(request.user.username)
    user_id = User.objects.get(username=request.user.username)
    # print(user_id.id)
    curr_user = UserProfileInfo.objects.get(id=user_id.id-1)
    (curr_user.visited) = True
    curr_user.visited_company_page = True
    curr_user.save()

    company = Company.objects.get(id=curr_user.company.id)
    total_views = UserProfileInfo.objects.filter(company=company,visited=True).count()
    user_object = UserProfileInfo.objects.filter(visited_company_page=True)
    currently_viewers = []
    for j in user_object:
        c = User.objects.filter(id=j.id+1)
        currently_viewers.append(c[0])
    count_hit = True
    # print(company.company_name)
    return render(request,'job/company.html',{'company':company,'total_views':total_views,'currently_viewers':currently_viewers})
    
@login_required
def special(request):
    curr_user = UserProfileInfo.objects.get(id=request.user.id-1)
    (curr_user.visited_company_page) = False
    curr_user.save()
    return HttpResponse("You are logged in !")
    
@login_required
def user_logout(request):
    curr_user = UserProfileInfo.objects.get(id=request.user.id-1)
    (curr_user.visited_company_page) = False
    curr_user.save()
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