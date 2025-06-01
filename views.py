from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth.decorators import login_required
#from ..forms import DataUserForm
from .models import DataUser

def logout_view(request):
    logout(request)  # Завершение сессии пользователя
    return redirect(reverse('login'))  # Переадресация на страницу логина

def login(request):
    if request.method == "POST":
        #action = request.POST.get('action')
        profile_name = request.POST.get('profile_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,profile_name=profile_name,username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Перенаправляем на страницу профиля
        else:
            messages.error(request, "Неверные данные для входа")  # Сообщение об ошибке
    return render(request, 'login/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username') # логин пользователя
        password = request.POST.get('password') # пароль пользователя
        password_confirm = request.POST.get('password_confirm') # повторный пароль пользователя
        email = request.POST.get('email') # эл.почта пользователя
        if password == password_confirm: # Проверка существующего пользователя
            if User.objects.filter(username=username).exists():
                messages.error(request, "Пользователь с таким именем уже существует")
            else:   
                user = User.objects.create_user( #Передача данных для создания профиля пользователя
                username=username, 
                password=password,
                email=email
                )
                user.save() #сохранение данных в базу данных
                messages.success(request, "Регистрация успешна! Теперь вы можете войти.") # уведомление о успешной регистрации
                return redirect('login')  # Перенаправляем на страницу входа после успешной регистрации
        else:
            messages.error(request, 'Пароли отличаются')
    return render(request,'registration/register.html') #перенаправление на ту же страницу при не действителынх данных

@login_required
def home(request):
    return render(request, 'home/home.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile/profile.html', {'user': user})

@login_required
def friends(request):
    return render(request, 'friends/friends.html')

@login_required
def about(request):
    return render(request, 'about/about.html')

@login_required
def chats(request):
    messages = Message.objects.order_by('-timestamp')[:50]  # История сообщений
    return render(request, 'chats/chats.html', {'messages': reversed(messages)})

@login_required
def edit_profile(request):
    user = get_object_or_404(User)
    if request.method == 'POST':
        form = DataUser(request.POST, instance=user)
        if form.is_valid():
            profile_name = request.POST.get('profile_name')  # Имя профиля
            age = request.POST.get('age') # возраст пользователя
            status = request.POST.get('status') # статус пользователя
            data_user = DataUser.objects.update_or_create(
                profile_name = profile_name,
                age = age,
                status = status
            )
            data_user.save()
            form.save()
            return redirect('login')