from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.contrib import messages
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import *

from .decorators import *
from .forms import *
from .models import *


# def home(request):
#     return render(request, 'home.html')

@unauthenticated_user
def SignUpView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User has been created", extra_tags="success")
            return redirect('login')
        else:
            messages.warning(request, "Failed to create user", extra_tags="warning")
            return redirect('register')
    else:
        form = SignUpForm()
    context={'form':form}
    return render(request, 'register.html', context)
    
@unauthenticated_user
def SignInView(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('checkin')
        else:
            messages.warning(request, "email or password is incorrect")
    return render(request, 'login.html')

def SignOutView(request):
    logout(request)
    return redirect('login')

@login_required(login_url='signin')
def ProfileView(request):
    return render(request, 'account/profile.html')

@login_required(login_url='signin')
def ProfileUpdateView(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated", extra_tags="success")
            return redirect('profile')
        else:
            messages.warning(request, "Failed to update your profile", extra_tags="warning")
    else:
        form = ProfileForm(instance=user)
    context = {'form':form}
    return render(request, 'account/profile_update.html', context)

@login_required(login_url='signin')
def ChangePasswordView(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, "Password has been changed", extra_tags="success")
        return redirect('userprofile')
    context={'form':form,}
    return render(request, 'account/change_password.html', context)

@login_required(login_url='signin')
@restricted_user
def PlaceCreateView(request):
    data = Place.objects.all()
    if request.method=='POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            form.city = request.POST.get("city")
            form.save()
            messages.success(request, "Place has been registered", extra_tags="success")
            return redirect('place_create')
        else:
            print(form.errors)
            messages.warning(request, "Failed to reqister", extra_tags="warning")
            return redirect('place_create')
    else:
        form = PlaceForm()
    context={'form':form, 'data':data}
    return render(request, 'place/placeform.html', context)

@login_required(login_url='signin')
@restricted_user
def PlaceDetailView(request,pk):
    data = Place.objects.get(id=pk)
    data2 = CheckIn.objects.filter(checkin_place=data.id)
    context = {'data':data , 'data2':data2}
    return render(request, 'place/place_detail.html', context)
    
@login_required(login_url='signin')
@restricted_user
def PlaceUpdateView(request,pk):
    place = Place.objects.get(id=pk)
    if request.method=='POST':
        form = PlaceForm(request.POST, request.FILES, instance=place )
        if form.is_valid():
            form.save()
            messages.success(request, "Place has been updated", extra_tags="success")
            return redirect('place_detail',pk=place.id)
        else:
            messages.warning(request, "Failed to update", extra_tags="warning")
            print(form.errors)
            return redirect('place_create')
    else:
        form = PlaceForm(instance=place)
    context={'form':form}
    return render(request, 'place/place_update.html', context)

@login_required(login_url='signin')
@restricted_user
def PlaceDeleteView(request,pk):
    data = Place.objects.get(id=pk)
    data2 = CheckIn.objects.filter(checkin_place=data.id)
    if request.method=='POST':
        data.delete()
        messages.success(request, "Place has been deleted", extra_tags="success")
        return redirect('place_create')
    context={'data':data, 'data2':data2}
    return render(request, 'place/place_delete.html', context)

@login_required(login_url='signin')
@restricted_user
def UserListView(request):
    data = User.objects.all()
    context={'data':data}
    return render(request, 'account/user_list.html', context)

@login_required(login_url='signin')
@restricted_user
def UserDetailView(request,pk):
    data = User.objects.get(id=pk)
    data2 = CheckIn.objects.filter(user=data.id)
    context = {'data':data, 'data2':data2}
    return render(request, 'account/user_detail.html', context)

@login_required(login_url='signin')
@restricted_user
def UserCheckInDeleteView(request,pk):
    data3 = CheckIn.objects.get(id=pk)
    data = User.objects.get(id=data3.user.id)
    data2 = CheckIn.objects.filter(user=data3.id)
    if request.method=='POST':
        data3.delete()
        messages.success(request, "Check In has been deleted", extra_tags="success")
        return redirect('user_detail', pk=data.id)
    context={'data':data, 'data2':data2, 'data3':data3 }
    return render(request, 'account/user_checkin_delete.html', context)

@login_required(login_url='signin')
def CheckInCreateView(request):
    data = request.user
    data2 = CheckIn.objects.filter(user=data.id)
    if request.method == 'POST':
        form = CheckInForm(request.POST,initial={'user':request.user})
        if form.is_valid():
            form.save()
            messages.success(request, "Check-In has been made", extra_tags="success")
            return redirect('checkin')
    else:
        form = CheckInForm(initial={'user':request.user})
    context = {'form':form, 'data2':data2}
    return render(request, 'checkin/checkin_form.html', context)
    
@login_required(login_url='signin')
@restricted_user
def CheckInDeleteView(request,pk):
    data = CheckIn.objects.get(id=pk)
    data3 = Place.objects.get(place=data.checkin_place)
    data2 = CheckIn.objects.filter(checkin_place=data3.id)
    if request.method=='POST':
        data.delete()
        messages.success(request, "Check In has been deleted", extra_tags="success")
        return redirect('place_detail', pk=data3.id)
    context={'data':data, 'data2':data2, 'data3':data3 }
    return render(request, 'checkin/checkin_delete.html', context)

@api_view(['GET'])
def CityApi(request,pk):
    city = City.objects.filter(province=pk)
    serializers = CitySerializers(city, many=True)
    return Response(serializers.data)

