from django.contrib.auth import views as auth_views
from django.conf.urls import *
from django.urls import path
from . import views
from .models import *

urlpatterns = [
    # path('', views.home, name="home"),
    path('register', views.SignUpView, name="register"),
    path('', views.SignInView, name="login"),
    path('logout', views.SignOutView, name="logout"),
    path('account/profile', views.ProfileView, name="profile"),
    path('account/profile/edit', views.ProfileUpdateView, name="profile_update"),
    path('account/change_password', views.ChangePasswordView, name='change_password'),


    path('place/create', views.PlaceCreateView, name="place_create"),
    path('place/<str:pk>', views.PlaceDetailView, name="place_detail"),
    path('place/<str:pk>/edit', views.PlaceUpdateView, name="place_update"),
    path('place/<str:pk>/delete', views.PlaceDeleteView, name="place_delete"),

    path('user/list', views.UserListView, name='user_list'),
    path('user/<str:pk>', views.UserDetailView, name='user_detail'),
    path('user/checkin/<str:pk>/delete', views.UserCheckInDeleteView, name='usercheckin_delete'),

    path('checkin', views.CheckInCreateView, name="checkin"),
    path('checkin/<str:pk>/delete', views.CheckInDeleteView, name="checkin_delete"),

    path('register/city/api/<str:pk>', views.CityApi, name="city_api")

]