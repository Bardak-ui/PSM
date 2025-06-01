from django.urls import path, reverse
from django.shortcuts import redirect
from . import views
from .views import logout_view

urlpatterns = [
    path('', lambda request: redirect(reverse('login'))),
    path('login/', views.login, name='login'),
    path('registration/', views.register, name="register"),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('friends/', views.friends, name='friends'),
    path('chats/', views.chats, name='chats'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
]