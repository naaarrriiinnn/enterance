from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def index(request):
    return render(request, 'index.html', {'title': 'index'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            htmly = get_template('Email.html')
            d = {'username': username}
            subject, from_email, to = 'hello', 'from@gmail.com', 'to@gmail.com'
            html_content = htmly.render(d)
            massege = EmailMultiAlternatives(subject, html_content, from_email, [to])
            massege.attach_alternative(html_content, "text/html")
            try:
                massege.send()
            except:
                print("error in sending mail")
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'reqister'})


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome  dear {username} !')
            return redirect('index')
        else:
            messages.info(request, f' this account does not exit ')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'log in'})
